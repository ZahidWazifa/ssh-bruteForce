"""
Logging utility for SSH Bruteforce Tool
"""

import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    """Enhanced logging class for SSH bruteforce operations"""
    
    def __init__(self, log_file: Optional[str] = None, log_level: str = "INFO"):
        """
        Initialize logger
        
        Args:
            log_file (str): Path to log file
            log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_file = log_file or "logs/ssh_bruteforce.log"
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger("SSHBruteforce")
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler for important messages
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        self.logger.addHandler(console_handler)
    
    def log_attempt(self, username: str, password: str, target: str):
        """
        Log a login attempt
        
        Args:
            username (str): Username attempted
            password (str): Password attempted
            target (str): Target host
        """
        message = f"ATTEMPT: {username}:{password} -> {target}"
        self.logger.info(message)
    
    def log_success(self, username: str, password: str, target: str):
        """
        Log a successful login
        
        Args:
            username (str): Successful username
            password (str): Successful password
            target (str): Target host
        """
        message = f"SUCCESS: {username}:{password} -> {target}"
        self.logger.info(message)
        
        # Also write to separate success file
        success_file = "logs/successful_logins.txt"
        os.makedirs(os.path.dirname(success_file), exist_ok=True)
        
        with open(success_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {target} - {username}:{password}\n")
    
    def log_error(self, error_message: str):
        """
        Log an error
        
        Args:
            error_message (str): Error message to log
        """
        self.logger.error(error_message)
    
    def log_warning(self, warning_message: str):
        """
        Log a warning
        
        Args:
            warning_message (str): Warning message to log
        """
        self.logger.warning(warning_message)
    
    def log_info(self, info_message: str):
        """
        Log an info message
        
        Args:
            info_message (str): Info message to log
        """
        self.logger.info(info_message)
    
    def log_debug(self, debug_message: str):
        """
        Log a debug message
        
        Args:
            debug_message (str): Debug message to log
        """
        self.logger.debug(debug_message)
    
    def log_attack_start(self, target: str, port: int, total_combinations: int):
        """
        Log the start of an attack
        
        Args:
            target (str): Target host
            port (int): Target port
            total_combinations (int): Total credential combinations
        """
        message = f"ATTACK START: Target={target}:{port}, Combinations={total_combinations}"
        self.logger.info(message)
    
    def log_attack_end(self, target: str, total_attempts: int, successful_logins: int, duration: float):
        """
        Log the end of an attack
        
        Args:
            target (str): Target host
            total_attempts (int): Total attempts made
            successful_logins (int): Number of successful logins
            duration (float): Attack duration in seconds
        """
        message = (f"ATTACK END: Target={target}, Attempts={total_attempts}, "
                  f"Successful={successful_logins}, Duration={duration:.2f}s")
        self.logger.info(message)
    
    def log_statistics(self, stats: dict):
        """
        Log attack statistics
        
        Args:
            stats (dict): Statistics dictionary
        """
        message = f"STATISTICS: {stats}"
        self.logger.info(message)
    
    def set_log_level(self, level: str):
        """
        Change logging level
        
        Args:
            level (str): New log level (DEBUG, INFO, WARNING, ERROR)
        """
        new_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(new_level)
        self.log_level = new_level
    
    def get_log_file_path(self) -> str:
        """
        Get the path to the log file
        
        Returns:
            str: Path to log file
        """
        return self.log_file
    
    def clear_logs(self):
        """Clear the log file"""
        try:
            with open(self.log_file, 'w') as f:
                f.write("")
            self.logger.info("Log file cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear log file: {e}")
    
    def export_logs(self, export_path: str):
        """
        Export logs to a different file
        
        Args:
            export_path (str): Path to export logs to
        """
        try:
            with open(self.log_file, 'r', encoding='utf-8') as source:
                with open(export_path, 'w', encoding='utf-8') as dest:
                    dest.write(source.read())
            self.logger.info(f"Logs exported to {export_path}")
        except Exception as e:
            self.logger.error(f"Failed to export logs: {e}")
