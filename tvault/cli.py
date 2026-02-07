#!/usr/bin/env python3
"""
CLI interface for TextVault
"""

import sys
import argparse
from pathlib import Path
from .vault import VaultManager
from .file import FileManager

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="TextVault - A lightweight text file management system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tvault vault add myvault /path/to/myvault
  tvault vault switch myvault
  tvault file create myfile
  tvault file read myfile
  tvault file update myfile --backup
        """
    )
    
    subparsers = parser.add_subparsers(dest="module", help="Module to use")
    
    # Vault module
    vault_parser = subparsers.add_parser("vault", help="Manage data directories")
    vault_subparsers = vault_parser.add_subparsers(dest="command", help="Vault command")
    
    # vault add
    add_parser = vault_subparsers.add_parser("add", help="Add a new data directory")
    add_parser.add_argument("name", help="Name of the data directory")
    add_parser.add_argument("path", help="Path to the data directory")
    
    # vault remove
    remove_parser = vault_subparsers.add_parser("remove", help="Remove a data directory from vaults.json")
    remove_parser.add_argument("name", help="Name of the data directory")
    
    # vault delete
    delete_parser = vault_subparsers.add_parser("delete", help="Delete a data directory from disk and vaults.json")
    delete_parser.add_argument("name", help="Name of the data directory")
    
    # vault switch
    switch_parser = vault_subparsers.add_parser("switch", help="Switch to a data directory")
    switch_parser.add_argument("name", help="Name of the data directory")
    
    # vault list
    vault_subparsers.add_parser("list", help="List all data directories")
    
    # vault current
    vault_subparsers.add_parser("current", help="Show current data directory")
    
    # vault dump
    dump_parser = vault_subparsers.add_parser("dump", help="Export a data directory to zip")
    dump_parser.add_argument("name", help="Name of the data directory")
    dump_parser.add_argument("target_path", help="Target path for zip file")
    
    # vault import
    import_parser = vault_subparsers.add_parser("import", help="Import a zip file as data directory")
    import_parser.add_argument("zip_path", help="Path to zip file")
    import_parser.add_argument("target_path", help="Target path for data directory")
    
    # File module
    file_parser = subparsers.add_parser("file", help="Manage files in current data directory")
    file_subparsers = file_parser.add_subparsers(dest="command", help="File command")
    
    # file create
    create_parser = file_subparsers.add_parser("create", help="Create a new file")
    create_parser.add_argument("filename", help="Name of the file")
    
    # file read
    read_parser = file_subparsers.add_parser("read", help="Read a file")
    read_parser.add_argument("filename", help="Name of the file")
    read_parser.add_argument("--backup", help="Read from backup (latest, N, YYYY_MM_DD, YYYY_MM_DD-hh:mm:ss)")
    
    # file update
    update_parser = file_subparsers.add_parser("update", help="Update a file")
    update_parser.add_argument("filename", help="Name of the file")
    update_parser.add_argument("--backup", action="store_true", help="Create backup before editing")
    update_parser.add_argument("--vim", action="store_true", help="Use vim instead of nano")
    
    # file delete
    delete_file_parser = file_subparsers.add_parser("delete", help="Delete a file")
    delete_file_parser.add_argument("filename", help="Name of the file")
    delete_file_parser.add_argument("--backup", nargs="?", const="all", help="Delete backups (all, N)")
    
    # file rename
    rename_parser = file_subparsers.add_parser("rename", help="Rename a file")
    rename_parser.add_argument("old_name", help="Old file name")
    rename_parser.add_argument("new_name", help="New file name")
    
    # file backup
    backup_parser = file_subparsers.add_parser("backup", help="Create backup of a file")
    backup_parser.add_argument("filename", help="Name of the file")
    
    # file recover
    recover_parser = file_subparsers.add_parser("recover", help="Recover file from backup")
    recover_parser.add_argument("filename", help="Name of the file")
    recover_parser.add_argument("backup_spec", help="Backup specification (latest, N, YYYY_MM_DD, YYYY_MM_DD-hh:mm:ss)")
    
    # file list
    file_subparsers.add_parser("list", help="List all files")
    
    args = parser.parse_args()
    
    if not args.module:
        parser.print_help()
        return 1
    
    try:
        if args.module == "vault":
            vault_manager = VaultManager()
            return handle_vault_command(vault_manager, args)
        elif args.module == "file":
            vault_manager = VaultManager()
            current_vault = vault_manager.get_current_vault()
            if not current_vault:
                print("Error: No current vault selected. Use 'tvault vault switch <name>' first.")
                return 1
            file_manager = FileManager(current_vault["path"])
            return handle_file_command(file_manager, args)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

def handle_vault_command(vault_manager, args):
    """Handle vault commands"""
    if args.command == "add":
        vault_manager.add_vault(args.name, args.path)
        print(f"Added vault '{args.name}' at {args.path}")
    elif args.command == "remove":
        vault_manager.remove_vault(args.name)
        print(f"Removed vault '{args.name}' from vaults.json")
    elif args.command == "delete":
        vault_manager.delete_vault(args.name)
        print(f"Deleted vault '{args.name}'")
    elif args.command == "switch":
        vault_manager.switch_vault(args.name)
        print(f"Switched to vault '{args.name}'")
    elif args.command == "list":
        vaults = vault_manager.list_vaults()
        if not vaults:
            print("No vaults found")
        else:
            for name, path in vaults.items():
                print(f"{name}: {path}")
    elif args.command == "current":
        current = vault_manager.get_current_vault()
        if current:
            print(f"{current['name']}: {current['path']}")
        else:
            print("No current vault selected")
    elif args.command == "dump":
        vault_manager.dump_vault(args.name, args.target_path)
        print(f"Dumped vault '{args.name}' to {args.target_path}")
    elif args.command == "import":
        name = vault_manager.import_vault(args.zip_path, args.target_path)
        print(f"Imported vault '{name}' from {args.zip_path}")
    else:
        print(f"Unknown vault command: {args.command}")
        return 1
    return 0

def handle_file_command(file_manager, args):
    """Handle file commands"""
    if args.command == "create":
        file_manager.create_file(args.filename)
        print(f"Created file '{args.filename}'")
    elif args.command == "read":
        content = file_manager.read_file(args.filename, args.backup)
        print(content)
    elif args.command == "update":
        file_manager.update_file(args.filename, args.backup, args.vim)
        print(f"Updated file '{args.filename}'")
    elif args.command == "delete":
        file_manager.delete_file(args.filename, args.backup)
        if args.backup is None:
            print(f"Deleted file '{args.filename}'")
        elif args.backup == "all":
            print(f"Deleted all backups for '{args.filename}'")
        else:
            print(f"Deleted {args.backup} oldest backup(s) for '{args.filename}'")
    elif args.command == "rename":
        file_manager.rename_file(args.old_name, args.new_name)
        print(f"Renamed '{args.old_name}' to '{args.new_name}'")
    elif args.command == "backup":
        file_manager.backup_file(args.filename)
        print(f"Created backup for '{args.filename}'")
    elif args.command == "recover":
        file_manager.recover_file(args.filename, args.backup_spec)
        print(f"Recovered '{args.filename}' from backup")
    elif args.command == "list":
        files = file_manager.list_files()
        if not files:
            print("No files found")
        else:
            for filename, backup_count in files.items():
                print(f"{filename}: {backup_count} backup(s)")
    else:
        print(f"Unknown file command: {args.command}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())