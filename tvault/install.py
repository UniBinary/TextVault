#!/usr/bin/env python3
"""
TextVault Installation Tools
"""

import os
import shutil
from pathlib import Path

def install():
    """Install tvault user-wide"""
    print("Installing tvault...")
    
    # Get paths
    script_dir = Path(__file__).parent
    home = Path.home()
    
    # Target directories
    bin_dir = home / ".local" / "bin"
    lib_dir = home / ".local" / "lib" / "tvault"
    
    # Create directories
    try:
        bin_dir.mkdir(parents=True, exist_ok=True)
        lib_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return False
    
    # Check if already installed
    tvault_bin = bin_dir / "tvault"
    tvault_py = lib_dir / "tvault.py"
    
    if tvault_bin.exists() or tvault_py.exists():
        print("Warning: tvault appears to be already installed.")
        response = input("Do you want to reinstall? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("Installation cancelled.")
            return False
    
    # Copy files
    try:
        # Copy shell script
        shutil.copy2(script_dir / "tvault", tvault_bin)
        os.chmod(tvault_bin, 0o755)  # Make executable
        
        # Copy Python script
        shutil.copy2(script_dir / "tvault.py", tvault_py)
        
        # Copy intro files
        intro_src = script_dir / "intros"
        intro_dst = lib_dir / "intros"
        if intro_src.exists():
            shutil.copytree(intro_src, intro_dst, dirs_exist_ok=True)
        
        print("Successfully installed tvault")
        print("Updating PATH if needed...")
    except Exception as e:
        print(f"Error during installation: {e}")
        return False


    try:
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
                            f.write(f"\n# Added by tvault installer\n{path_line}\n")
                        print(f"Added PATH to: {config}")
                        path_updated = True
                    else:
                        print(f"PATH already set in: {config}")
                        path_updated = True
                except Exception:
                    pass
        
        if not path_updated:
            print("Warning: Unable to update PATH")
            print(f"Please add this line to your shell config: {path_line}")
        
        print("\nInstallation complete!")
        print("Usage: tvault <operation> <filename>")
        print('Try "tvault --help" for more information')
        return True
        
    except Exception as e:
        print(f"Error during PATH updating: {e}")
        return False
