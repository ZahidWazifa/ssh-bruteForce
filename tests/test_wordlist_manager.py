"""
Unit tests for WordlistManager module
"""

import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.wordlist_manager import WordlistManager


class TestWordlistManager(unittest.TestCase):
    """Test cases for WordlistManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.wm = WordlistManager()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test WordlistManager initialization"""
        self.assertIsInstance(self.wm, WordlistManager)
        self.assertIsNotNone(self.wm.base_dir)
        self.assertIsNotNone(self.wm.wordlists_dir)
    
    def test_load_wordlist_from_file(self):
        """Test loading wordlist from file"""
        # Create temporary wordlist file
        test_file = os.path.join(self.temp_dir, "test_words.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("admin\n")
            f.write("root\n")
            f.write("# this is a comment\n")
            f.write("user\n")
            f.write("\n")  # empty line
            f.write("guest\n")
        
        words = self.wm.load_wordlist(test_file)
        
        expected = ["admin", "root", "user", "guest"]
        self.assertEqual(words, expected)
    
    def test_load_wordlist_file_not_found(self):
        """Test loading wordlist from non-existent file"""
        words = self.wm.load_wordlist("nonexistent_users.txt")
        
        # Should return default user wordlist
        self.assertIsInstance(words, list)
        self.assertIn("root", words)
        self.assertIn("admin", words)
    
    def test_load_default_credentials(self):
        """Test loading default credentials"""
        # Create temporary credentials file
        test_file = os.path.join(self.temp_dir, "test_creds.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("admin:password\n")
            f.write("root:root\n")
            f.write("# comment line\n")
            f.write("guest:guest\n")
        
        creds = self.wm.load_default_credentials(test_file)
        
        expected = [("admin", "password"), ("root", "root"), ("guest", "guest")]
        self.assertEqual(creds, expected)
    
    def test_load_default_credentials_file_not_found(self):
        """Test loading default credentials from non-existent file"""
        creds = self.wm.load_default_credentials("nonexistent.txt")
        
        # Should return hardcoded defaults
        self.assertIsInstance(creds, list)
        self.assertTrue(len(creds) > 0)
        self.assertIn(("root", "root"), creds)
        self.assertIn(("admin", "admin"), creds)
    
    def test_create_custom_wordlist(self):
        """Test creating custom wordlist"""
        words = ["test1", "test2", "test3"]
        output_file = os.path.join(self.temp_dir, "custom_test.txt")
        
        self.wm.create_custom_wordlist(words, output_file)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Verify content
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read().strip().split('\n')
        
        self.assertEqual(content, words)
    
    def test_merge_wordlists(self):
        """Test merging multiple wordlists"""
        # Create test files
        file1 = os.path.join(self.temp_dir, "list1.txt")
        file2 = os.path.join(self.temp_dir, "list2.txt")
        output_file = os.path.join(self.temp_dir, "merged.txt")
        
        with open(file1, 'w') as f:
            f.write("admin\nroot\nuser\n")
        
        with open(file2, 'w') as f:
            f.write("guest\nroot\ntest\n")  # 'root' is duplicate
        
        self.wm.merge_wordlists([file1, file2], output_file, remove_duplicates=True)
        
        # Verify merged file
        merged_words = self.wm.load_wordlist(output_file)
        self.assertEqual(len(merged_words), 5)  # Should have 5 unique words
        self.assertIn("admin", merged_words)
        self.assertIn("root", merged_words)
        self.assertIn("guest", merged_words)
    
    def test_shuffle_wordlist(self):
        """Test shuffling wordlist"""
        original = ["word1", "word2", "word3", "word4", "word5"]
        shuffled = self.wm.shuffle_wordlist(original)
        
        # Should have same length and elements
        self.assertEqual(len(shuffled), len(original))
        self.assertEqual(set(shuffled), set(original))
        
        # Original should be unchanged
        self.assertEqual(original, ["word1", "word2", "word3", "word4", "word5"])
    
    def test_filter_wordlist(self):
        """Test filtering wordlist"""
        words = ["a", "ab", "abc", "abcd", "test", "testing"]
        
        # Test length filter
        filtered = self.wm.filter_wordlist(words, min_length=3, max_length=4)
        expected = ["abc", "abcd", "test"]
        self.assertEqual(filtered, expected)
        
        # Test contains filter
        filtered = self.wm.filter_wordlist(words, contains="test")
        expected = ["test", "testing"]
        self.assertEqual(filtered, expected)
    
    def test_get_wordlist_stats(self):
        """Test getting wordlist statistics"""
        words = ["a", "bb", "ccc", "dd", "e"]
        stats = self.wm.get_wordlist_stats(words)
        
        expected = {
            "count": 5,
            "min_length": 1,
            "max_length": 3,
            "avg_length": 1.8,
            "unique_count": 5
        }
        self.assertEqual(stats, expected)
    
    def test_get_wordlist_stats_empty(self):
        """Test getting stats for empty wordlist"""
        stats = self.wm.get_wordlist_stats([])
        self.assertEqual(stats, {"count": 0})
    
    def test_generate_mutations(self):
        """Test generating password mutations"""
        base_words = ["password"]
        mutations = self.wm.generate_mutations(base_words)
        
        # Should contain original and various mutations
        self.assertIn("password", mutations)
        self.assertIn("Password", mutations)
        self.assertIn("PASSWORD", mutations)
        self.assertIn("password1", mutations)
        self.assertIn("password123", mutations)
        self.assertIn("password2024", mutations)
        self.assertIn("drowssap", mutations)  # reversed
        
        # Should be a list of unique values
        self.assertEqual(len(mutations), len(set(mutations)))
    
    def test_get_default_wordlist_users(self):
        """Test getting default user wordlist"""
        words = self.wm._get_default_wordlist("common_users.txt")
        
        self.assertIsInstance(words, list)
        self.assertIn("root", words)
        self.assertIn("admin", words)
    
    def test_get_default_wordlist_passwords(self):
        """Test getting default password wordlist"""
        words = self.wm._get_default_wordlist("common_passwords.txt")
        
        self.assertIsInstance(words, list)
        self.assertIn("password", words)
        self.assertIn("123456", words)
    
    def test_get_default_credentials_hardcoded(self):
        """Test getting hardcoded default credentials"""
        creds = self.wm._get_default_credentials()
        
        self.assertIsInstance(creds, list)
        self.assertTrue(len(creds) > 0)
        
        # Check that all items are tuples with 2 elements
        for cred in creds:
            self.assertIsInstance(cred, tuple)
            self.assertEqual(len(cred), 2)


class TestWordlistManagerIntegration(unittest.TestCase):
    """Integration tests for WordlistManager"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.wm = WordlistManager()
    
    def test_load_existing_wordlists(self):
        """Test loading actual wordlist files if they exist"""
        # This test will pass even if files don't exist due to fallback behavior
        users = self.wm.load_wordlist("common_users.txt")
        passwords = self.wm.load_wordlist("common_passwords.txt")
        
        self.assertIsInstance(users, list)
        self.assertIsInstance(passwords, list)
        self.assertTrue(len(users) > 0)
        self.assertTrue(len(passwords) > 0)
    
    def test_workflow_create_and_load(self):
        """Test creating and loading custom wordlist"""
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp()
        try:
            # Create custom wordlist
            custom_words = ["custom1", "custom2", "custom3"]
            output_file = os.path.join(temp_dir, "test_custom.txt")
            
            self.wm.create_custom_wordlist(custom_words, output_file)
            
            # Load it back
            loaded_words = self.wm.load_wordlist(output_file)
            
            self.assertEqual(loaded_words, custom_words)
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
