#!/usr/bin/env python3
"""
TextVault (TVault) - A lightweight text file management system
Version: 1.0.0.1
Author: GQX
License: MIT
"""

import sys
import shutil
from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from pyotp import TOTP

class TextVault:
    """Main TextVault class"""
    
    def __init__(self, data_dir=None):
        """Initialize the vault"""
        if data_dir is None:
            self.data_dir = Path.home() / ".local" / "lib" / "tdb"
        else:
            self.data_dir = Path(data_dir)
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, filename):
        """Get full path for a file (adds .txt extension)"""
        return self.data_dir / f"{filename}.txt"
    
    def _get_backup_path(self, filename):
        """Get backup file path"""
        return self._get_file_path(filename).with_suffix(".txt.bak")
    
    def _print_totp_if_needed(self, filename, content):
        """Print TOTP if filename contains 'tt'"""
        if "tt" in filename:
            try:
                print(f"TOTP: {TOTP(content).now()}")
            except Exception:
                print("Warning: Could not generate TOTP. Printing content instead:")
                print(content)
        else:
            print(content)
    
    def create(self, filename, force=False):
        """Create a new text file"""
        filepath = self._get_file_path(filename)
        
        if filepath.exists() and not force:
            response = input(
                "Warning: The file already exists!\n"
                "Press [ENTER] to cancel, or enter any character to overwrite: "
            )
            if not response:
                print("Operation cancelled.")
                return False
        
        try:
            filepath.touch()
            print(f"Created file: {filename}")
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def read(self, filename):
        """Read content from a file"""
        filepath = self._get_file_path(filename)
        
        if not filepath.exists():
            print(f"Error: File '{filename}' does not exist!")
            return False
        
        try:
            content = filepath.read_text(encoding="utf-8")
            self._print_totp_if_needed(filename, content)
            return True
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def write(self, filename):
        """Write content to a file (with backup)"""
        filepath = self._get_file_path(filename)
        backup_path = self._get_backup_path(filename)
        
        if not filepath.exists():
            print(f"Error: File '{filename}' does not exist!")
            return False
        
        try:
            # Read existing content and create backup
            content = filepath.read_text(encoding="utf-8")
            backup_path.write_text(content, encoding="utf-8")
            
            # Show current content
            print("Current content:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Get new content
            print("Enter new content (empty line to finish):")
            lines = []
            while True:
                line = input(">>> ")
                if line == "":
                    break
                lines.append(line)
            
            # Write new content
            filepath.write_text("\n".join(lines), encoding="utf-8")
            print(f"File '{filename}' updated successfully.")
            return True
            
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    def backup(self, filename):
        """Create a backup of a file"""
        filepath = self._get_file_path(filename)
        backup_path = self._get_backup_path(filename)
        
        if not filepath.exists():
            print(f"Error: File '{filename}' does not exist!")
            return False
        
        try:
            content = filepath.read_text(encoding="utf-8")
            backup_path.write_text(content, encoding="utf-8")
            print(f"Backup created for '{filename}'")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def recover(self, filename):
        """Recover file from backup"""
        filepath = self._get_file_path(filename)
        backup_path = self._get_backup_path(filename)
        
        if not backup_path.exists():
            print(f"Error: Backup for '{filename}' does not exist!")
            return False
        
        try:
            content = backup_path.read_text(encoding="utf-8")
            print("Backup content:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            response = input("Are you sure you want to restore from backup? (yes/no): ")
            if response.lower() in ["yes", "y", "1"]:
                filepath.write_text(content, encoding="utf-8")
                backup_path.unlink()  # Remove backup after recovery
                print(f"File '{filename}' recovered from backup.")
                return True
            else:
                print("Recovery cancelled.")
                return False
                
        except Exception as e:
            print(f"Error recovering file: {e}")
            return False
    
    def remove(self, filename):
        """Remove a file"""
        filepath = self._get_file_path(filename)
        
        if not filepath.exists():
            print(f"Error: File '{filename}' does not exist!")
            return False
        
        try:
            filepath.unlink()
            print(f"File '{filename}' removed.")
            return True
        except Exception as e:
            print(f"Error removing file: {e}")
            return False
    
    def remove_backup(self, filename):
        """Remove a backup file"""
        backup_path = self._get_backup_path(filename)
        
        if not backup_path.exists():
            print(f"Error: Backup for '{filename}' does not exist!")
            return False
        
        try:
            backup_path.unlink()
            print(f"Backup for '{filename}' removed.")
            return True
        except Exception as e:
            print(f"Error removing backup: {e}")
            return False
    
    def read_backup(self, filename):
        """Read content from backup"""
        backup_path = self._get_backup_path(filename)
        
        if not backup_path.exists():
            print(f"Error: Backup for '{filename}' does not exist!")
            return False
        
        try:
            content = backup_path.read_text(encoding="utf-8")
            self._print_totp_if_needed(filename, content)
            return True
        except Exception as e:
            print(f"Error reading backup: {e}")
            return False
    
    def list_files(self):
        """List all files in the database"""
        try:
            files = list(self.data_dir.glob("*.txt"))
            if not files:
                print("No files in database.")
                return True
            
            print(f"Files in database ({len(files)} total):")
            print("-" * 40)
            for file in sorted(files):
                size = file.stat().st_size
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                backup_exists = file.with_suffix(".txt.bak").exists()
                backup_marker = "✓" if backup_exists else " "
                print(f"{backup_marker} {file.stem:20} {size:6} bytes  {mtime:%Y-%m-%d %H:%M}")
            return True
            
        except Exception as e:
            print(f"Error listing files: {e}")
            return False
    
    def backup_database(self):
        """Backup the entire database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path.home() / f"tdb_backup_{timestamp}"
            
            shutil.copytree(self.data_dir, backup_dir)
            print(f"Database backed up to: {backup_dir}")
            return True
        except Exception as e:
            print(f"Error backing up database: {e}")
            return False
    
    def remove_database(self):
        """Remove the entire database"""
        response = input(
            "WARNING: This will remove ALL TDB files and uninstall the package!\n"
            "Type 'confirm-delete-all' to proceed: "
        )
        
        if response == "confirm-delete-all":
            try:
                # Remove database directory
                if self.data_dir.exists():
                    shutil.rmtree(self.data_dir)
                
                # Remove binary
                bin_path = Path.home() / ".local" / "bin" / "tdb"
                if bin_path.exists():
                    bin_path.unlink()
                
                print("TDB removed successfully.")
                print("Note: To uninstall the Python package, run: pip3 uninstall textvault")
                return True
            except Exception as e:
                print(f"Error removing database: {e}")
                return False
        else:
            print("Operation cancelled.")
            return False


def main():
    """Main entry point"""
    parser = ArgumentParser(
        description="Text Database - A lightweight text file management system",
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "operation",
        choices=[
            "create", "read", "write", "backup", "recover",
            "remove", "removebak", "readbak", "list", "dumpdb", "rmdb"
        ],
        help="Operation to perform"
    )
    
    parser.add_argument(
        "filename",
        nargs="?",
        help="Filename (without .txt extension)"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite when creating new files"
    )
    
    parser.add_argument(
        "--data-dir",
        help="Custom data directory (default: ~/.local/lib/tdb)"
    )
    
    args = parser.parse_args()
    
    # Validate filename for operations that need it
    operations_needing_filename = [
        "create", "read", "write", "backup", "recover",
        "remove", "removebak", "readbak"
    ]
    
    if args.operation in operations_needing_filename and not args.filename:
        print(f"Error: Operation '{args.operation}' requires a filename!")
        parser.print_help()
        return 1
    
    # Initialize database
    db = TextVault(args.data_dir)
    
    # Execute operation
    operations = {
        "create": lambda: db.create(args.filename, args.force),
        "read": lambda: db.read(args.filename),
        "write": lambda: db.write(args.filename),
        "backup": lambda: db.backup(args.filename),
        "recover": lambda: db.recover(args.filename),
        "remove": lambda: db.remove(args.filename),
        "removebak": lambda: db.remove_backup(args.filename),
        "readbak": lambda: db.read_backup(args.filename),
        "list": lambda: db.list_files(),
        "dumpdb": lambda: db.backup_database(),
        "rmdb": lambda: db.remove_database(),
    }
    
    success = operations.get(args.operation, lambda: False)()
    return 0 if success else 1


if __name__ == "__main__":
    # Prevent direct imports
    sys.exit(main())
else:
    # Allow imports for testing purposes
    # raise ImportError("This module should not to be imported directly, use the 'tvault' command instead.")
    pass  # Allow imports for testing and development
