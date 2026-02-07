# UniBinaryTextVault (TVault)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)]()

A lightweight, command-line text file management system with multi-vault support and automatic backups.

**Version: 2.1**

**Note**: The project is actively maintained and improved.

## ✨ New Features in 2.0

- **Multi-vault support**: Manage multiple data directories (vaults)
- **Enhanced backup system**: Timestamp-based backups with flexible recovery options
- **Modular architecture**: Separate vault and file management modules
- **Advanced file operations**: Rename, bulk backup deletion, and more
- **Zip import/export**: Easily transfer vaults between systems

## 📦 Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip3 install UniBinaryTextVault
```

### Method 2: Install from source

```bash
git clone https://github.com/UniBinary/TextVault.git
cd TextVault
pip3 install .
```

## 🚀 Quick Start

```bash
# Create a new vault
tvault vault add myvault ~/Documents/myvault

# Switch to the vault
tvault vault switch myvault

# Create a new file
tvault file create notes

# Write content to the file (opens nano editor)
tvault file update notes

# Read the file
tvault file read notes

# Create a backup
tvault file backup notes

# List all files
tvault file list

# Get help
tvault --help
```

## 📖 Usage

**Note**: There are some **usage examples** at the end of the document.


### Vault Management

| Command | Description | Example |
|---------|-------------|---------|
| `tvault vault add <name> <path>` | Add a new vault | `tvault vault add work ~/work_vault` |
| `tvault vault remove <name>` | Remove vault from registry | `tvault vault remove work` |
| `tvault vault delete <name>` | Delete vault from disk and registry | `tvault vault delete work` |
| `tvault vault switch <name>` | Switch to a vault | `tvault vault switch work` |
| `tvault vault list` | List all vaults | `tvault vault list` |
| `tvault vault current` | Show current vault | `tvault vault current` |
| `tvault vault dump <name> <path>` | Export vault to zip | `tvault vault dump work backup.zip` |
| `tvault vault import <zip> <path>` | Import zip as vault | `tvault vault import backup.zip ~/new_vault` |

### File Management

| Command | Description | Example |
|---------|-------------|---------|
| `tvault file create <file>` | Create a new file | `tvault file create notes` |
| `tvault file read <file>` | Read file content | `tvault file read notes` |
| `tvault file read <file> --backup <spec>` | Read from backup | `tvault file read notes --backup latest` |
| `tvault file update <file>` | Edit file with nano | `tvault file update notes` |
| `tvault file update <file> --backup` | Edit with backup | `tvault file update notes --backup` |
| `tvault file update <file> --vim` | Edit with vim | `tvault file update notes --vim` |
| `tvault file delete <file>` | Delete file | `tvault file delete notes` |
| `tvault file delete <file> --backup` | Delete all backups | `tvault file delete notes --backup` |
| `tvault file delete <file> --backup N` | Delete N oldest backups | `tvault file delete notes --backup 3` |
| `tvault file rename <old> <new>` | Rename file | `tvault file rename notes memos` |
| `tvault file backup <file>` | Create backup | `tvault file backup notes` |
| `tvault file recover <file> <spec>` | Recover from backup | `tvault file recover notes latest` |
| `tvault file list` | List all files | `tvault file list` |

### Backup Specification

The `--backup` option accepts several formats:
- `latest`: The most recent backup
- `N`: The Nth backup (1 = newest, 2 = second newest, etc.)
- `YYYY_MM_DD`: Backup from specific date
- `YYYY_MM_DD-hh:mm:ss`: Backup from specific date and time


## 🗂️ Data Structure

### Configuration Files
```
~/.local/lib/tvault/
├── vaults.json          # Vault registry
└── current.txt          # Current vault info
```

### Vault Structure
```
vault_directory/
├── index.json           # File index with backup counts
├── file1/
│   ├── file1            # Main file
│   ├── file1_20250207-124639.bak
│   └── file1_20250206-184937.bak
└── file2/
    ├── file2
    └── file2_20250107-014846.bak
```

### File Formats

**vaults.json:**
```json
{
  "default": "/Users/user/.local/lib/tvault/default",
  "work": "/Users/user/Documents/work_vault"
}
```

**current.txt:**
```
work
/Users/user/Documents/work_vault
```

**index.json:**
```json
{
  "notes": 3,
  "memos": 1
}
```

## 🛠️ Development

### Project Structure

```
textvault/
├── tvault/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # CLI interface
│   ├── vault.py         # Vault management
│   ├── file.py          # File management
│   └── __main__.py      # Main entry point
├── setup.py             # Installation configuration
├── README.md            # This file
└── LICENSE              # MIT License
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Reporting Issues

If you encounter any issues, please:

1. Check the [existing issues](https://github.com/UniBinary/TextVault/issues)
2. Create a new issue with:
   - A clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Author**: UniBinary
- **Email**: tp114514251@outlook.com
- **GitHub**: [UniBinary](https://github.com/UniBinary)
- **GitHub Project**: [TextVault](https://github.com/UniBinary/TextVault)
- **PyPI**: [UniBinaryTextVault](https://pypi.org/project/UniBinaryTextVault/)
- **Issues**: [GitHub Issues](https://github.com/UniBinary/TextVault/issues)

## 🙏 Acknowledgments

- Thanks to all contributors and users
- Built with Python's standard library

## 📦 Dependencies

TextVault requires the following Python packages:
- `pyotp>=2.6.0` (for potential future TOTP support)

These are automatically installed when using `pip install UniBinaryTextVault`.



# UniBinaryTextVault (TVault) - Usage Examples

## 🏦 Multi-Vault Management

### 1. Setting Up Multiple Vaults
```bash
# Create a personal vault
tvault vault add personal ~/Documents/personal_vault

# Create a work vault
tvault vault add work ~/Documents/work_vault

# Create a project vault
tvault vault add project ~/Projects/notes_vault

# List all vaults
tvault vault list
# Output:
# personal: /Users/user/Documents/personal_vault
# work: /Users/user/Documents/work_vault
# project: /Users/user/Projects/notes_vault

# Switch to work vault
tvault vault switch work

# Check current vault
tvault vault current
# Output:
# work: /Users/user/Documents/work_vault
```

### 2. Exporting and Importing Vaults
```bash
# Export work vault to zip file
tvault vault dump work ~/Desktop/work_backup.zip

# Import the backup as a new vault
tvault vault import ~/Desktop/work_backup.zip ~/Documents/work_archive

# The new vault will be automatically added
tvault vault list
# Output will include: work_archive: /Users/user/Documents/work_archive
```

## 📁 File Management

### 3. Basic File Operations
```bash
# Make sure you're in the right vault
tvault vault switch personal

# Create a new file
tvault file create daily_notes

# Edit the file (opens nano by default)
tvault file update daily_notes
# Add some content and save

# Read the file
tvault file read daily_notes

# Create a backup
tvault file backup daily_notes

# List all files in current vault
tvault file list
# Output:
# daily_notes: 1
```

### 4. Advanced Backup Operations
```bash
# Create multiple backups
tvault file backup daily_notes
tvault file backup daily_notes
tvault file backup daily_notes

# Check backup count
tvault file list
# Output: daily_notes: 3

# Read from specific backup
tvault file read daily_notes --backup latest
tvault file read daily_notes --backup 2  # Second newest backup
tvault file read daily_notes --backup 2025_02_07  # Backup from specific date

# Delete the oldest backup
tvault file delete daily_notes --backup 1

# Check updated backup count
tvault file list
# Output: daily_notes: 2

# Delete all backups
tvault file delete daily_notes --backup

# Check final backup count
tvault file list
# Output: daily_notes: 0
```

### 5. File Editing with Different Editors
```bash
# Edit with nano (default)
tvault file update config --backup  # Creates backup before editing

# Edit with vim
tvault file update script.py --vim

# Edit with vim and create backup
tvault file update important.txt --vim --backup
```

### 6. File Recovery
```bash
# Accidentally overwrote a file? Recover from backup!
tvault file recover important_doc latest

# Recover from specific backup
tvault file recover report 2025_02_06-14:30:00
```

### 7. File Organization
```bash
# Create multiple files
tvault file create meeting_notes
tvault file create todo_list
tvault file create ideas

# Rename a file
tvault file rename meeting_notes meeting_20250207

# Delete a file
tvault file delete old_notes
```

## 🔄 Workflow Examples

### 8. Daily Journal Workflow
```bash
# Switch to personal vault
tvault vault switch personal

# Create today's journal entry
tvault file create journal_$(date +%Y%m%d)

# Edit the journal
tvault file update journal_$(date +%Y%m%d) --backup

# At the end of the day, create a final backup
tvault file backup journal_$(date +%Y%m%d)
```

### 9. Project Documentation
```bash
# Switch to project vault
tvault vault switch project

# Create project documentation
tvault file create README
tvault file create API_DOCS
tvault file create CHANGELOG

# Work on API documentation
tvault file update API_DOCS --vim --backup

# After major changes, create backups
tvault file backup README
tvault file backup API_DOCS
```

### 10. Code Snippet Management
```bash
# Create files for different languages
tvault file create python_snippets
tvault file create javascript_snippets
tvault file create sql_queries

# Add a new Python snippet
tvault file update python_snippets
# Add: # Fibonacci function
# Add: def fibonacci(n):
# Add:     if n <= 1:
# Add:         return n
# Add:     return fibonacci(n-1) + fibonacci(n-2)

# Create backup before major reorganization
tvault file backup python_snippets
```

## 🚨 Emergency Scenarios

### 11. Recovering from Accidental Deletion
```bash
# Oops! Deleted the wrong file
# First, check if you have backups
tvault file list
# If backup count > 0, you can recover

# Recover from latest backup
tvault file recover important_file latest

# If that doesn't work, try older backups
tvault file recover important_file 2
tvault file recover important_file 2025_02_06
```

### 12. Migrating to a New Computer
```bash
# On old computer: export all vaults
tvault vault dump personal ~/Desktop/personal_backup.zip
tvault vault dump work ~/Desktop/work_backup.zip

# On new computer: install TextVault
pip3 install UniBinaryTextVault

# Import vaults
tvault vault import ~/Desktop/personal_backup.zip ~/Documents/personal
tvault vault import ~/Desktop/work_backup.zip ~/Documents/work

# Switch to your preferred vault
tvault vault switch personal
```

## 💡 Tips and Best Practices

1. **Regular Backups**: Use `--backup` flag when editing important files
2. **Meaningful Names**: Use descriptive file names
3. **Vault Organization**: Separate personal, work, and project files
4. **Clean Up**: Periodically delete old backups with `tvault file delete <file> --backup N`
5. **Export Regularly**: Use `tvault vault dump` for important vaults

## 🐛 Troubleshooting

### Common Issues and Solutions

**Issue**: "Error: No current vault selected"
**Solution**: Use `tvault vault switch <vault_name>` to select a vault first

**Issue**: "Editor not found"
**Solution**: Install nano or vim: `sudo apt install nano` (Linux) or `brew install nano` (macOS)

**Issue**: "File not found"
**Solution**: Check current vault with `tvault vault current` and file list with `tvault file list`

**Issue**: "Invalid backup specification"
**Solution**: Use one of: `latest`, `N` (number), `YYYY_MM_DD`, or `YYYY_MM_DD-hh:mm:ss`