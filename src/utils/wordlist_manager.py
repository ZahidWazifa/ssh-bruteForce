"""
Wordlist management utility for SSH Bruteforce Tool
"""

import os
import random
from typing import List, Tuple, Optional


class WordlistManager:
    """Wordlist management class for handling usernames and passwords"""
    
    def __init__(self):
        """Initialize WordlistManager"""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.wordlists_dir = os.path.join(self.base_dir, "wordlists")
    
    def load_wordlist(self, filepath: str) -> List[str]:
        """
        Load wordlist from file
        
        Args:
            filepath (str): Path to wordlist file
            
        Returns:
            List[str]: List of words from the file
        """
        # If filepath is relative, make it relative to wordlists directory
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.wordlists_dir, filepath)
        
        words = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip comments and empty lines
                        words.append(line)
        except FileNotFoundError:
            print(f"Warning: Wordlist file not found: {filepath}")
            return self._get_default_wordlist(os.path.basename(filepath))
        except Exception as e:
            print(f"Error loading wordlist {filepath}: {e}")
            return []
        
        return words
    
    def _get_default_wordlist(self, filename: str) -> List[str]:
        """
        Get default wordlist if file is not found
        
        Args:
            filename (str): Name of the wordlist file
            
        Returns:
            List[str]: Default wordlist
        """
        if "user" in filename.lower():
            return ["root", "admin", "administrator", "user", "guest", "test", "oracle", "postgres"]
        elif "pass" in filename.lower():
            return ["password", "123456", "admin", "root", "guest", "test", "password123", ""]
        else:
            return []
    
    def load_default_credentials(self, filepath: Optional[str] = None) -> List[Tuple[str, str]]:
        """
        Load default credential combinations
        
        Args:
            filepath (str): Path to default credentials file
            
        Returns:
            List[Tuple[str, str]]: List of (username, password) tuples
        """
        if filepath is None:
            filepath = os.path.join(self.wordlists_dir, "default_creds.txt")
        
        credentials = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            username, password = line.split(':', 1)
                            credentials.append((username.strip(), password.strip()))
        except FileNotFoundError:
            print(f"Warning: Default credentials file not found: {filepath}")
            return self._get_default_credentials()
        except Exception as e:
            print(f"Error loading default credentials: {e}")
            return []
        
        return credentials
    
    def _get_default_credentials(self) -> List[Tuple[str, str]]:
        """
        Get hardcoded default credentials
        
        Returns:
            List[Tuple[str, str]]: List of default (username, password) combinations
        """
        return [
            ("root", "root"),
            ("admin", "admin"),
            ("administrator", "administrator"),
            ("root", ""),
            ("admin", ""),
            ("guest", "guest"),
            ("test", "test"),
            ("user", "user"),
            ("oracle", "oracle"),
            ("postgres", "postgres"),
            ("mysql", "mysql"),
            ("ftp", "ftp"),
            ("pi", "raspberry"),
            ("ubuntu", "ubuntu"),
            ("root", "toor"),
            ("admin", "password"),
            ("root", "password"),
            ("admin", "123456"),
            ("root", "123456")
        ]
    
    def create_custom_wordlist(self, words: List[str], output_file: str):
        """
        Create a custom wordlist file
        
        Args:
            words (List[str]): List of words to write
            output_file (str): Output file path
        """
        try:
            # Ensure the custom directory exists
            custom_dir = os.path.join(self.wordlists_dir, "custom")
            os.makedirs(custom_dir, exist_ok=True)
            
            # If output_file is just a filename, put it in custom directory
            if not os.path.dirname(output_file):
                output_file = os.path.join(custom_dir, output_file)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for word in words:
                    f.write(f"{word}\n")
            
            print(f"Custom wordlist created: {output_file}")
            
        except Exception as e:
            print(f"Error creating custom wordlist: {e}")
    
    def merge_wordlists(self, wordlist_files: List[str], output_file: str, 
                       remove_duplicates: bool = True):
        """
        Merge multiple wordlists into one
        
        Args:
            wordlist_files (List[str]): List of wordlist file paths
            output_file (str): Output file path
            remove_duplicates (bool): Whether to remove duplicate entries
        """
        merged_words = []
        
        for filepath in wordlist_files:
            words = self.load_wordlist(filepath)
            merged_words.extend(words)
        
        if remove_duplicates:
            merged_words = list(set(merged_words))
        
        self.create_custom_wordlist(merged_words, output_file)
    
    def shuffle_wordlist(self, wordlist: List[str]) -> List[str]:
        """
        Shuffle wordlist order
        
        Args:
            wordlist (List[str]): Original wordlist
            
        Returns:
            List[str]: Shuffled wordlist
        """
        shuffled = wordlist.copy()
        random.shuffle(shuffled)
        return shuffled
    
    def filter_wordlist(self, wordlist: List[str], min_length: int = 1, 
                       max_length: int = None, contains: str = None) -> List[str]:
        """
        Filter wordlist based on criteria
        
        Args:
            wordlist (List[str]): Original wordlist
            min_length (int): Minimum word length
            max_length (int): Maximum word length
            contains (str): String that word must contain
            
        Returns:
            List[str]: Filtered wordlist
        """
        filtered = []
        
        for word in wordlist:
            # Check length constraints
            if len(word) < min_length:
                continue
            if max_length and len(word) > max_length:
                continue
            
            # Check contains constraint
            if contains and contains.lower() not in word.lower():
                continue
            
            filtered.append(word)
        
        return filtered
    
    def get_wordlist_stats(self, wordlist: List[str]) -> dict:
        """
        Get statistics about a wordlist
        
        Args:
            wordlist (List[str]): Wordlist to analyze
            
        Returns:
            dict: Statistics dictionary
        """
        if not wordlist:
            return {"count": 0}
        
        lengths = [len(word) for word in wordlist]
        
        return {
            "count": len(wordlist),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "avg_length": sum(lengths) / len(lengths),
            "unique_count": len(set(wordlist))
        }
    
    def generate_mutations(self, base_words: List[str]) -> List[str]:
        """
        Generate password mutations from base words
        
        Args:
            base_words (List[str]): Base words to mutate
            
        Returns:
            List[str]: List of mutations
        """
        mutations = []
        
        for word in base_words:
            # Original word
            mutations.append(word)
            
            # Common mutations
            mutations.append(word.capitalize())
            mutations.append(word.upper())
            mutations.append(word.lower())
            
            # Number suffixes
            for i in range(10):
                mutations.append(f"{word}{i}")
                mutations.append(f"{word}0{i}")
            
            # Year suffixes
            for year in range(2020, 2026):
                mutations.append(f"{word}{year}")
            
            # Common suffixes
            suffixes = ["123", "321", "!", "@", "#", "$", "1", "01", "001"]
            for suffix in suffixes:
                mutations.append(f"{word}{suffix}")
            
            # Reverse
            mutations.append(word[::-1])
        
        return list(set(mutations))  # Remove duplicates
    
    def list_available_wordlists(self) -> List[str]:
        """
        List all available wordlist files
        
        Returns:
            List[str]: List of available wordlist file paths
        """
        wordlists = []
        
        try:
            for root, dirs, files in os.walk(self.wordlists_dir):
                for file in files:
                    if file.endswith('.txt'):
                        rel_path = os.path.relpath(os.path.join(root, file), self.wordlists_dir)
                        wordlists.append(rel_path)
        except Exception as e:
            print(f"Error listing wordlists: {e}")
        
        return sorted(wordlists)
