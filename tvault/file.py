#!/usr/bin/env python3
"""
File management module
"""

import json
import shutil
import subprocess
import os
from pathlib import Path
from datetime import datetime
import re

class FileManager:
    """Manage files in a data directory"""
    
    def __init__(self, data_dir):
        """Initialize file manager with data directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.data_dir / "index.json"
        self._init_index()
    
    def _init_index(self):
        """Initialize index.json if not exists"""
        if not self.index_file.exists():
            with open(self.index_file, 'w') as f:
                json.dump({}, f, indent=2)
    
    def _load_index(self):
        """Load index from JSON file"""
        with open(self.index_file, 'r') as f:
            return json.load(f)
    
    def _save_index(self, index):
        """Save index to JSON file"""
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)
    
    def _get_file_dir(self, filename):
        """Get directory for a file"""
        return self.data_dir / filename
    
    def _get_file_path(self, filename):
        """Get path to main file"""
        return self._get_file_dir(filename) / filename
    
    def _get_backup_pattern(self, filename):
        """Get backup file pattern"""
        return f"{filename}_*.bak"
    
    def _parse_backup_spec(self, filename, backup_spec):
        """Parse backup specification"""
        file_dir = self._get_file_dir(filename)
        if not file_dir.exists():
            raise ValueError(f"File '{filename}' not found")
        
        # Get all backup files
        backup_files = list(file_dir.glob(f"{filename}_*.bak"))
        if not backup_files:
            raise ValueError(f"No backups found for '{filename}'")
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if backup_spec == "latest":
            return backup_files[0]
        
        # Try to parse as number
        try:
            n = int(backup_spec)
            if n <= 0 or n > len(backup_files):
                raise ValueError(f"Backup number {n} out of range (1-{len(backup_files)})")
            return backup_files[n-1]
        except ValueError:
            pass
        
        # Try to parse as date/time
        try:
            # Try YYYY_MM_DD-hh:mm:ss
            if "-" in backup_spec and ":" in backup_spec:
                # Format: YYYY_MM_DD-hh:mm:ss
                date_str, time_str = backup_spec.split("-")
                # Convert to backup filename format: YYYYMMDD-HHMMSS
                date_part = date_str.replace("_", "")
                time_part = time_str.replace(":", "")
                pattern = f"{filename}_{date_part}-{time_part}.bak"
            elif "-" in backup_spec:
                # Format: YYYY_MM_DD-hh:mm:ss (but no colon, maybe just date)
                # Actually this is just YYYY_MM_DD format
                date_str = backup_spec
                date_part = date_str.replace("_", "")
                pattern = f"{filename}_{date_part}-*.bak"
            else:
                # Try YYYY_MM_DD
                date_part = backup_spec.replace("_", "")
                pattern = f"{filename}_{date_part}-*.bak"
            
            matching_files = list(file_dir.glob(pattern))
            if not matching_files:
                raise ValueError(f"No backup found matching '{backup_spec}'")
            
            # Return the first matching file
            return matching_files[0]
        except Exception:
            raise ValueError(f"Invalid backup specification: {backup_spec}")
    
    def create_file(self, filename):
        """Create a new file"""
        file_dir = self._get_file_dir(filename)
        if file_dir.exists():
            raise ValueError(f"File '{filename}' already exists")
        
        file_dir.mkdir(parents=True)
        file_path = self._get_file_path(filename)
        file_path.touch()
        
        # Update index
        index = self._load_index()
        index[filename] = 0
        self._save_index(index)
    
    def read_file(self, filename, backup_spec=None):
        """Read a file or backup"""
        if backup_spec:
            backup_file = self._parse_backup_spec(filename, backup_spec)
            return backup_file.read_text()
        else:
            file_path = self._get_file_path(filename)
            if not file_path.exists():
                raise ValueError(f"File '{filename}' not found")
            return file_path.read_text()
    
    def update_file(self, filename, create_backup=False, use_vim=False):
        """Update a file using editor"""
        file_path = self._get_file_path(filename)
        if not file_path.exists():
            raise ValueError(f"File '{filename}' not found")
        
        # Create backup if requested
        if create_backup:
            self.backup_file(filename)
        
        # Choose editor
        editor = "vim" if use_vim else "nano"
        
        # Edit file
        try:
            # Set TERM environment variable if not set
            env = os.environ.copy()
            if "TERM" not in env:
                env["TERM"] = "xterm"
            
            subprocess.run([editor, str(file_path)], check=True, env=env)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Editor failed: {e}")
        except FileNotFoundError:
            raise RuntimeError(f"Editor '{editor}' not found. Please install it.")
    
    def delete_file(self, filename, backup_spec=None):
        """Delete a file or backups"""
        file_dir = self._get_file_dir(filename)
        if not file_dir.exists():
            raise ValueError(f"File '{filename}' not found")
        
        index = self._load_index()
        
        if backup_spec is None:
            # Delete entire file directory
            shutil.rmtree(file_dir)
            del index[filename]
        elif backup_spec == "all":
            # Delete all backups
            backup_files = list(file_dir.glob(f"{filename}_*.bak"))
            for backup in backup_files:
                backup.unlink()
            index[filename] = 0
        else:
            # Delete N oldest backups
            try:
                n = int(backup_spec)
                if n <= 0:
                    raise ValueError("Number of backups to delete must be positive")
                
                backup_files = list(file_dir.glob(f"{filename}_*.bak"))
                if not backup_files:
                    raise ValueError(f"No backups found for '{filename}'")
                
                # Sort by modification time (oldest first)
                backup_files.sort(key=lambda x: x.stat().st_mtime)
                
                # Delete oldest N backups
                deleted = 0
                for i in range(min(n, len(backup_files))):
                    backup_files[i].unlink()
                    deleted += 1
                
                # Update index
                current_count = index.get(filename, 0)
                index[filename] = max(0, current_count - deleted)
            except ValueError as e:
                raise ValueError(f"Invalid backup specification: {e}")
        
        self._save_index(index)
    
    def rename_file(self, old_name, new_name):
        """Rename a file"""
        old_dir = self._get_file_dir(old_name)
        if not old_dir.exists():
            raise ValueError(f"File '{old_name}' not found")
        
        new_dir = self._get_file_dir(new_name)
        if new_dir.exists():
            raise ValueError(f"File '{new_name}' already exists")
        
        # Rename directory
        old_dir.rename(new_dir)
        
        # Rename main file
        old_file = new_dir / old_name
        new_file = new_dir / new_name
        if old_file.exists():
            old_file.rename(new_file)
        
        # Rename backup files
        for backup in new_dir.glob(f"{old_name}_*.bak"):
            new_backup_name = backup.name.replace(f"{old_name}_", f"{new_name}_")
            backup.rename(new_dir / new_backup_name)
        
        # Update index
        index = self._load_index()
        if old_name in index:
            index[new_name] = index[old_name]
            del index[old_name]
            self._save_index(index)
    
    def backup_file(self, filename):
        """Create backup of a file"""
        file_path = self._get_file_path(filename)
        if not file_path.exists():
            raise ValueError(f"File '{filename}' not found")
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{filename}_{timestamp}.bak"
        backup_path = self._get_file_dir(filename) / backup_name
        
        # Copy file
        shutil.copy2(file_path, backup_path)
        
        # Update index
        index = self._load_index()
        current_count = index.get(filename, 0)
        index[filename] = current_count + 1
        self._save_index(index)
    
    def recover_file(self, filename, backup_spec):
        """Recover file from backup"""
        backup_file = self._parse_backup_spec(filename, backup_spec)
        file_path = self._get_file_path(filename)
        
        # Copy backup to main file
        shutil.copy2(backup_file, file_path)
    
    def list_files(self):
        """List all files"""
        index = self._load_index()
        return index