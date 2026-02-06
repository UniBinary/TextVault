#!/usr/bin/env python3
"""
TextVault Development Tools
"""

import os
import sys
import shutil
from pathlib import Path

def read_intro_file(filename):
    """Read a file from the intros directory"""
    intro_dir = Path(__file__).parent / "intros"
    filepath = intro_dir / filename
    
    if not filepath.exists():
        print(f"Error: File '{filename}' not found in intros directory")
        return None
    
    try:
        return filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def readme():
    """Display the README"""
    content = read_intro_file("README.md")
    if content:
        print(content)

def license():
    """Display the LICENSE"""
    content = read_intro_file("LICENSE")
    if content:
        print(content)

def run():
    """Interactive development mode"""
    print("TDB Development Mode")
    print("Available commands: readme, license, exit")
    print("-" * 40)
    
    while True:
        try:
            command = input("(tdb-dev)>>> ").strip()
            
            if command == "exit":
                print("Exiting development mode.")
                break
            elif command == "readme":
                readme()
            elif command == "license":
                license()
            elif command:
                print(f"Unknown command: {command}")
                print("Available: readme, license, exit")
                
        except KeyboardInterrupt:
            print("\nExiting development mode.")
            break
        except EOFError:
            print("\nExiting development mode.")
            break

def install():
    """Install TDB system-wide"""
    print("Installing Text Database (TDB)...")
    
    # Get paths
    script_dir = Path(__file__).parent
    home = Path.home()
    
    # Target directories
    bin_dir = home / ".local" / "bin"
    lib_dir = home / ".local" / "lib" / "tdb"
    
    # Create directories
    try:
        bin_dir.mkdir(parents=True, exist_ok=True)
        lib_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return False
    
    # Check if already installed
    tdb_bin = bin_dir / "tdb"
    tdb_py = lib_dir / "tdb.py"
    
    if tdb_bin.exists() or tdb_py.exists():
        print("Warning: TDB appears to be already installed.")
        response = input("Do you want to reinstall? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("Installation cancelled.")
            return False
    
    # Copy files
    try:
        # Copy shell script
        shutil.copy2(script_dir / "tdb", tdb_bin)
        os.chmod(tdb_bin, 0o755)  # Make executable
        
        # Copy Python script
        shutil.copy2(script_dir / "tdb.py", tdb_py)
        
        # Copy intro files
        intro_src = script_dir / "intros"
        intro_dst = lib_dir / "intros"
        if intro_src.exists():
            shutil.copytree(intro_src, intro_dst, dirs_exist_ok=True)
        
        print(f"✓ Script installed to: {tdb_bin}")
        print(f"✓ Library installed to: {lib_dir}")
        
        # Check if PATH needs updating
        shell_configs = [
            home / ".bashrc",
            home / ".zshrc",
            home / ".bash_profile",
            home / ".profile",
        ]
        
        path_updated = False
        path_line = 'export PATH="$PATH:$HOME/.local/bin"'
        
        for config in shell_configs:
            if config.exists():
                try:
                    content = config.read_text()
                    if path_line not in content and "$HOME/.local/bin" not in content:
                        with open(config, "a") as f:
                            f.write(f"\n# Added by TDB installer\n{path_line}\n")
                        print(f"✓ Added PATH to: {config}")
                        path_updated = True
                except Exception:
                    pass
        
        if not path_updated:
            print("⚠  Please ensure ~/.local/bin is in your PATH")
            print(f"   Add this line to your shell config: {path_line}")
        
        print("\nInstallation complete!")
        print("Usage: tdb <operation> <filename>")
        print("Try: tdb --help for more information")
        return True
        
    except Exception as e:
        print(f"Error during installation: {e}")
        return False


if __name__ == "__main__":
    print("TDB Development Tools")
    print("This module is for development purposes.")
    print("To install TextVault, run: from tvault.dev import install; install()")
    print("To use TDB, run: tdb <operation> <filename>")