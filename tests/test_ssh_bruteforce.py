"""
Unit tests for SSH Bruteforce module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ssh_bruteforce import SSHBruteforce
from config import Config


class TestSSHBruteforce(unittest.TestCase):
    """Test cases for SSHBruteforce class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.target_host = "192.168.1.100"
        self.port = 22
        self.bruteforcer = SSHBruteforce(
            target_host=self.target_host,
            port=self.port,
            timeout=1,
            max_threads=2
        )
    
    def test_initialization(self):
        """Test SSH bruteforce initialization"""
        self.assertEqual(self.bruteforcer.target_host, self.target_host)
        self.assertEqual(self.bruteforcer.port, self.port)
        self.assertEqual(self.bruteforcer.timeout, 1)
        self.assertEqual(self.bruteforcer.max_threads, 2)
        self.assertEqual(self.bruteforcer.attempts, 0)
        self.assertEqual(len(self.bruteforcer.found_credentials), 0)
    
    @patch('ssh_bruteforce.paramiko.SSHClient')
    def test_ssh_connect_success(self, mock_ssh_client):
        """Test successful SSH connection"""
        # Mock successful connection
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        mock_client.connect.return_value = None
        
        result = self.bruteforcer.ssh_connect("admin", "password")
        
        self.assertTrue(result)
        mock_client.connect.assert_called_once_with(
            hostname=self.target_host,
            port=self.port,
            username="admin",
            password="password",
            timeout=1
        )
        mock_client.close.assert_called_once()
    
    @patch('ssh_bruteforce.paramiko.SSHClient')
    def test_ssh_connect_auth_failure(self, mock_ssh_client):
        """Test SSH connection authentication failure"""
        # Mock authentication failure
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        mock_client.connect.side_effect = paramiko.AuthenticationException()
        
        result = self.bruteforcer.ssh_connect("admin", "wrongpass")
        
        self.assertFalse(result)
    
    @patch('ssh_bruteforce.paramiko.SSHClient')
    def test_ssh_connect_connection_error(self, mock_ssh_client):
        """Test SSH connection error"""
        # Mock connection error
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        mock_client.connect.side_effect = Exception("Connection refused")
        
        result = self.bruteforcer.ssh_connect("admin", "password")
        
        self.assertFalse(result)
    
    def test_load_credential_combinations(self):
        """Test loading credential combinations"""
        # Mock wordlist manager
        with patch.object(self.bruteforcer.wordlist_manager, 'load_wordlist') as mock_load, \
             patch.object(self.bruteforcer.wordlist_manager, 'load_default_credentials') as mock_default:
            
            mock_load.side_effect = [["admin", "root"], ["password", "123456"]]
            mock_default.return_value = [("guest", "guest")]
            
            self.bruteforcer.load_credential_combinations()
            
            # Should have 2*2 + 1 = 5 combinations
            self.assertEqual(self.bruteforcer.queue.qsize(), 5)
    
    @patch('ssh_bruteforce.tqdm')
    @patch.object(SSHBruteforce, 'ssh_connect')
    def test_worker_thread_success(self, mock_ssh_connect, mock_tqdm):
        """Test worker thread with successful login"""
        mock_progress = Mock()
        mock_tqdm.return_value = mock_progress
        mock_ssh_connect.return_value = True
        
        # Add test credentials to queue
        self.bruteforcer.queue.put(("admin", "password"))
        
        # Run worker
        self.bruteforcer.worker(mock_progress)
        
        # Check results
        self.assertEqual(len(self.bruteforcer.found_credentials), 1)
        self.assertEqual(self.bruteforcer.found_credentials[0], ("admin", "password"))
        self.assertEqual(self.bruteforcer.attempts, 1)
    
    @patch('ssh_bruteforce.tqdm')
    @patch.object(SSHBruteforce, 'ssh_connect')
    def test_worker_thread_failure(self, mock_ssh_connect, mock_tqdm):
        """Test worker thread with failed login"""
        mock_progress = Mock()
        mock_tqdm.return_value = mock_progress
        mock_ssh_connect.return_value = False
        
        # Add test credentials to queue
        self.bruteforcer.queue.put(("admin", "wrongpass"))
        
        # Run worker
        self.bruteforcer.worker(mock_progress)
        
        # Check results
        self.assertEqual(len(self.bruteforcer.found_credentials), 0)
        self.assertEqual(self.bruteforcer.attempts, 1)
    
    def test_config_integration(self):
        """Test integration with Config class"""
        self.assertIsInstance(self.bruteforcer.config, Config)
        self.assertIsNotNone(self.bruteforcer.config.get('ssh.timeout'))
    
    @patch('ssh_bruteforce.threading.Thread')
    @patch('ssh_bruteforce.tqdm')
    @patch.object(SSHBruteforce, 'load_credential_combinations')
    def test_run_method(self, mock_load_creds, mock_tqdm, mock_thread):
        """Test run method"""
        mock_progress = Mock()
        mock_tqdm.return_value = mock_progress
        mock_load_creds.return_value = None
        
        # Mock queue size
        self.bruteforcer.queue.qsize = Mock(return_value=5)
        
        # Mock thread
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        # Run with minimal setup
        with patch('builtins.print'):  # Suppress print output
            self.bruteforcer.run()
        
        # Verify thread creation and start
        self.assertTrue(mock_thread.called)
        self.assertTrue(mock_thread_instance.start.called)


class TestSSHBruteforceIntegration(unittest.TestCase):
    """Integration tests for SSH Bruteforce"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.bruteforcer = SSHBruteforce("127.0.0.1", port=22, timeout=1, max_threads=1)
    
    def test_full_workflow_mock(self):
        """Test full workflow with mocked SSH connections"""
        with patch.object(self.bruteforcer, 'ssh_connect') as mock_connect, \
             patch.object(self.bruteforcer.wordlist_manager, 'load_wordlist') as mock_load, \
             patch.object(self.bruteforcer.wordlist_manager, 'load_default_credentials') as mock_default, \
             patch('ssh_bruteforce.tqdm') as mock_tqdm, \
             patch('builtins.print'):  # Suppress output
            
            # Setup mocks
            mock_load.side_effect = [["admin"], ["password"]]
            mock_default.return_value = []
            mock_connect.return_value = True  # Simulate success
            mock_progress = Mock()
            mock_tqdm.return_value = mock_progress
            
            # Run the attack
            self.bruteforcer.run()
            
            # Verify results
            self.assertEqual(len(self.bruteforcer.found_credentials), 1)
            self.assertEqual(self.bruteforcer.found_credentials[0], ("admin", "password"))


if __name__ == '__main__':
    # Add paramiko import for tests
    try:
        import paramiko
    except ImportError:
        print("Warning: paramiko not installed, some tests may fail")
        paramiko = Mock()
        paramiko.AuthenticationException = Exception
    
    unittest.main(verbosity=2)
