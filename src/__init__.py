"""
SSH Bruteforce Tool Package
"""

__version__ = "1.0.0"
__author__ = "Security Researcher"
__email__ = "researcher@example.com"

from .ssh_bruteforce import SSHBruteforce
from .config import Config

__all__ = ["SSHBruteforce", "Config"]
