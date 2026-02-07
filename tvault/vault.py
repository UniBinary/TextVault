#!/usr/bin/env python3
"""
Vault management module
"""

import json
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

class VaultManager:
    """Manage multiple data directories (vaults)"""
    
    def __init__(self):
        """Initialize vault manager"""
        self.base_dir = Path.home() / ".local" / "lib" / "tvault"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.vaults_file = self.base_dir / "vaults.json"
        self.current_file = self.base_dir / "current.txt"
        
        # Initialize default vault if not exists
        self._init_default_vault()
    
    def _init_default_vault(self):
        """Initialize default vault if needed"""
        if not self.vaults_file.exists():
            default_vault_path = self.base_dir / "default"
            default_vault_path.mkdir(parents=True, exist_ok=True)
            
            vaults = {"default": str(default_vault_path)}
            self._save_vaults(vaults)
    
    def _load_vaults(self):
        """Load vaults from JSON file"""
        if not self.vaults_file.exists():
            return {}
        
        with open(self.vaults_file, 'r') as f:
            return json.load(f)
    
    def _save_vaults(self, vaults):
        """Save vaults to JSON file"""
        with open(self.vaults_file, 'w') as f:
            json.dump(vaults, f, indent=2)
    
    def _get_current_vault_info(self):
        """Get current vault name and path"""
        if not self.current_file.exists():
            return None
        
        with open(self.current_file, 'r') as f:
            lines = f.read().strip().split('\n')
            if len(lines) >= 2:
                return {"name": lines[0], "path": lines[1]}
        return None
    
    def add_vault(self, name, path):
        """Add a new vault"""
        vaults = self._load_vaults()
        
        if name in vaults:
            raise ValueError(f"Vault '{name}' already exists")
        
        path_obj = Path(path).expanduser().resolve()
        path_obj.mkdir(parents=True, exist_ok=True)
        
        vaults[name] = str(path_obj)
        self._save_vaults(vaults)
    
    def remove_vault(self, name):
        """Remove a vault from vaults.json"""
        vaults = self._load_vaults()
        
        if name not in vaults:
            raise ValueError(f"Vault '{name}' not found")
        
        # Check if it's the current vault
        current = self._get_current_vault_info()
        if current and current["name"] == name:
            # Clear current vault
            self.current_file.unlink(missing_ok=True)
        
        del vaults[name]
        self._save_vaults(vaults)
    
    def delete_vault(self, name):
        """Delete a vault from disk and vaults.json"""
        vaults = self._load_vaults()
        
        if name not in vaults:
            raise ValueError(f"Vault '{name}' not found")
        
        path = Path(vaults[name])
        
        # Check if it's the current vault
        current = self._get_current_vault_info()
        if current and current["name"] == name:
            # Clear current vault
            self.current_file.unlink(missing_ok=True)
        
        # Delete from disk
        if path.exists():
            shutil.rmtree(path)
        
        # Remove from vaults
        del vaults[name]
        self._save_vaults(vaults)
    
    def switch_vault(self, name):
        """Switch to a vault"""
        vaults = self._load_vaults()
        
        if name not in vaults:
            raise ValueError(f"Vault '{name}' not found")
        
        path = Path(vaults[name])
        if not path.exists():
            raise ValueError(f"Vault path does not exist: {path}")
        
        # Save current vault
        with open(self.current_file, 'w') as f:
            f.write(f"{name}\n{path}\n")
    
    def list_vaults(self):
        """List all vaults"""
        return self._load_vaults()
    
    def get_current_vault(self):
        """Get current vault"""
        info = self._get_current_vault_info()
        if not info:
            return None
        
        vaults = self._load_vaults()
        if info["name"] not in vaults:
            return None
        
        return {
            "name": info["name"],
            "path": Path(info["path"])
        }
    
    def dump_vault(self, name, target_path):
        """Export a vault to zip file"""
        vaults = self._load_vaults()
        
        if name not in vaults:
            raise ValueError(f"Vault '{name}' not found")
        
        source_path = Path(vaults[name])
        if not source_path.exists():
            raise ValueError(f"Vault path does not exist: {source_path}")
        
        target_path = Path(target_path).expanduser().resolve()
        
        # Create zip file
        with zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_path)
                    zipf.write(file_path, arcname)
    
    def import_vault(self, zip_path, target_path):
        """Import a zip file as vault"""
        zip_path = Path(zip_path).expanduser().resolve()
        if not zip_path.exists():
            raise ValueError(f"Zip file not found: {zip_path}")
        
        target_path = Path(target_path).expanduser().resolve()
        if target_path.exists():
            raise ValueError(f"Target path already exists: {target_path}")
        
        # Extract zip
        target_path.mkdir(parents=True)
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(target_path)
        
        # Generate vault name from target path
        vault_name = target_path.name
        
        # Add to vaults
        vaults = self._load_vaults()
        if vault_name in vaults:
            # Add suffix if name exists
            i = 1
            while f"{vault_name}_{i}" in vaults:
                i += 1
            vault_name = f"{vault_name}_{i}"
        
        vaults[vault_name] = str(target_path)
        self._save_vaults(vaults)
        
        return vault_name