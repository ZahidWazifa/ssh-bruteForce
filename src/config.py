"""
Configuration module for SSH Bruteforce Tool
"""

import yaml
import os
from typing import Dict, Any


class Config:
    """Configuration management class"""
    
    def __init__(self, config_file=None):
        """
        Initialize configuration
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file or "config.yaml"
        self.config_data = self._load_default_config()
        
        # Load from file if exists
        if os.path.exists(self.config_file):
            self._load_config_file()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "ssh": {
                "default_port": 22,
                "timeout": 5,
                "max_retries": 3
            },
            "bruteforce": {
                "max_threads": 10,
                "delay_between_attempts": 0.1,
                "stop_on_first_success": False
            },
            "logging": {
                "log_level": "INFO",
                "log_file": "logs/ssh_bruteforce.log",
                "log_attempts": True,
                "log_successes": True,
                "log_errors": True
            },
            "wordlists": {
                "default_userlist": "wordlists/common_users.txt",
                "default_passlist": "wordlists/common_passwords.txt",
                "default_creds": "wordlists/default_creds.txt"
            },
            "output": {
                "save_results": True,
                "results_file": "logs/results.txt",
                "verbose": True
            }
        }
    
    def _load_config_file(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    self._merge_configs(self.config_data, file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
    
    def _merge_configs(self, default: Dict, override: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in override.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_configs(default[key], value)
            else:
                default[key] = value
    
    def get(self, key: str, default=None):
        """
        Get configuration value using dot notation
        
        Args:
            key (str): Configuration key (e.g., 'ssh.timeout')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key (str): Configuration key (e.g., 'ssh.timeout')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self, filepath=None):
        """
        Save current configuration to file
        
        Args:
            filepath (str): Path to save config file
        """
        filepath = filepath or self.config_file
        
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_data, f, default_flow_style=False, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data"""
        return self.config_data.copy()
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.config_data = self._load_default_config()
    
    def validate_config(self) -> bool:
        """
        Validate current configuration
        
        Returns:
            bool: True if configuration is valid
        """
        try:
            # Check required sections
            required_sections = ['ssh', 'bruteforce', 'logging', 'wordlists']
            for section in required_sections:
                if section not in self.config_data:
                    print(f"Missing required config section: {section}")
                    return False
            
            # Validate specific values
            if self.get('ssh.timeout', 0) <= 0:
                print("SSH timeout must be positive")
                return False
            
            if self.get('bruteforce.max_threads', 0) <= 0:
                print("Max threads must be positive")
                return False
            
            return True
            
        except Exception as e:
            print(f"Config validation error: {e}")
            return False
