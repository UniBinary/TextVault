# TextVault (TVault) - Usage Examples

## 📝 Basic Usage

### 1. Managing Notes
```bash
# Create a notes file
tvault new my-notes

# Write some notes
tvault write my-notes
# Enter your notes line by line, empty line to finish

# Read your notes
tvault read my-notes

# Create a backup
tvault backup my-notes

# List all your files
tvault list
```

### 2. Password Management (with TOTP)
```bash
# Store a TOTP secret
tvault new my-totp-secrets
tvault write my-totp-secrets
# Enter: JBSWY3DPEHPK3PXP  # Example TOTP secret

# When you need the code
tvault read my-totp-secrets
# Output: TOTP: 123456
```

### 3. Configuration Files
```bash
# Store application configurations
tvault new app-config
tvault write app-config
# Enter configuration line by line

# Backup before making changes
tvault backup app-config

# If something goes wrong, recover
tvault recover app-config
```

## 🔧 Advanced Scenarios

### 1. Script Integration
```bash
#!/bin/bash
# backup-script.sh

# Backup important files daily
tvault backup server-config
tvault backup database-settings

# Create timestamped backup of entire database
tvault dumpdb

echo "Backup completed at $(date)"
```

### 2. Python Integration
```python
#!/usr/bin/env python3
# integrate_with_python.py

import subprocess
import json

def get_tdb_file(filename):
    """Read a TVault file from Python"""
    result = subprocess.run(
        ["tdb", "read", filename],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None

def write_tdb_file(filename, content):
    """Write to a TVault file from Python"""
    # Create the file first
    subprocess.run(["tdb", "new", filename, "--force"])
    
    # For simple content, we could write directly
    # For complex content, consider using the interactive mode
    print(f"Please run: tvault write {filename}")
    print(f"And enter: {content}")

# Example usage
if __name__ == "__main__":
    # Store API keys securely
    config = {
        "api_key": "sk-1234567890",
        "endpoint": "https://api.example.com"
    }
    
    write_tdb_file("api-config", json.dumps(config, indent=2))
    
    # Later, read it back
    content = get_tdb_file("api-config")
    if content:
        print(f"Config: {content}")
```

### 3. Automated Backups with Cron
```bash
# Add to crontab (crontab -e)
# Daily backup at 2 AM
0 2 * * * /usr/local/bin/tvault dumpdb

# Hourly backup of critical files
0 * * * * /usr/local/bin/tvault backup important-config
30 * * * * /usr/local/bin/tvault backup user-data
```

## 🎯 Real-World Use Cases

### 1. Development Environment Setup
```bash
# Store development environment variables
tvault new dev-env
tvault write dev-env
# Enter:
# DATABASE_URL=postgres://user:pass@localhost/dev
# API_KEY=dev_key_123
# DEBUG=true

# Use in scripts
export $(tvault read dev-env | xargs)
```

### 2. Meeting Notes
```bash
# Before meeting
tvault new meeting-2024-01-15
tvault write meeting-2024-01-15
# Enter agenda items

# During meeting
tvault write meeting-2024-01-15
# Add notes

# After meeting
tvault backup meeting-2024-01-15
tvault read meeting-2024-01-15
```

### 3. Personal Journal
```bash
# Daily journal entry
DATE=$(date +%Y-%m-%d)
tvault new journal-$DATE
tvault write journal-$DATE
# Write your thoughts

# Monthly review
tvault list | grep journal-2024-01
```

### 4. Code Snippets Library
```bash
# Store useful code snippets
tvault new python-snippets
tvault write python-snippets
# Enter your favorite code snippets

tvault new bash-snippets
tvault write bash-snippets
# Enter useful bash commands

# When you need a snippet
tvault read python-snippets | grep "function"
```

## ⚠️ Best Practices

### 1. Naming Conventions
```bash
# Use descriptive names
tvault new project-configuration  # Good
tvault new config                 # Less descriptive

# Use consistent naming
tvault new journal-2024-01-15     # Date-based
tvault new meeting-team-weekly    # Purpose-based
```

### 2. Regular Backups
```bash
# Backup important files regularly
tvault backup critical-data
tvault backup important-settings

# Schedule automatic backups
# See cron examples above
```

### 3. Security Considerations
```bash
# Don't store highly sensitive data without encryption
# TVault files are plain text

# Use TOTP for 2FA secrets
tvault new auth-totp-secrets
tvault write auth-totp-secrets
# Store TOTP seeds here

# Regular cleanup
tvault remove temp-notes
tvault removebak old-backups
```

### 4. Organization
```bash
# List and review regularly
tvault list

# Archive old files
tvault backup old-project-notes
tvault remove old-project-notes

# Keep database clean
# Remove unused files
```

## 🔄 Migration Examples

### From Plain Text Files
```bash
# If you have existing text files
cp ~/notes.txt ~/.local/lib/tdb/notes.txt

# Now you can use TVault with them
tvault read notes
tvault backup notes
```

### To New System
```bash
# Backup everything before migration
tvault dumpdb

# The backup will be in ~/tdb_backup_YYYYMMDD_HHMMSS/
# You can restore files from there if needed
```

## 🆘 Troubleshooting

### Common Issues and Solutions

1. **"Command not found: tdb"**
   ```bash
   # Ensure ~/.local/bin is in your PATH
   echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **"Error: File does not exist!"**
   ```bash
   # Create the file first
   tvault new filename
   ```

3. **Backup not working**
   ```bash
   # Check if file exists
   tvault read filename
   
   # Manually check backup
   ls -la ~/.local/lib/tdb/*.bak
   ```

4. **TOTP not generating codes**
   ```bash
   # Ensure filename contains "tt"
   tvault new my-tt-secrets
   
   # Ensure secret is valid Base32
   tvault write my-tt-secrets
   # Enter: JBSWY3DPEHPK3PXP (valid Base32)
   ```

## 📊 Performance Tips

1. **Keep files small**: TVault works best with text files under 1MB
2. **Regular cleanup**: Remove unused files and backups
3. **Use meaningful names**: Makes `tvault list` more useful
4. **Batch operations**: Use scripts for repetitive tasks

---

For more information, run:
```bash
tvault --help
```

Or check the main README.md file.