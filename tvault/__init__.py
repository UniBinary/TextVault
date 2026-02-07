"""
TextVault - A lightweight text file management system
Version: 2.1
"""

__version__ = "2.1"
__author__ = "UniBinary"
__license__ = "MIT"

from .cli import main
from .vault import VaultManager
from .file import FileManager

__all__ = ["main", "VaultManager", "FileManager"]