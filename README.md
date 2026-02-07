# UniBinaryTextVault (TVault)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)]()

A lightweight, command-line text file management system with automatic backup support.

**Version: 1.1**

## ✨ Features

- **Simple CRUD operations**: Create, read, update, and delete text files
- **Automatic backups**: Every write operation creates a backup
- **TOTP support**: Generate time-based one-time passwords from files containing "tt" in their names
- **Cross-platform**: Works on Linux, macOS, and Windows
- **No database required**: Uses plain text files
- **Easy to use**: Simple command-line interface

## 📦 Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip3 install UniBinaryTextVault
```

### Method 2: Install from source

```bash
git clone https://github.com/UniBinary/TextVault.git
pip3 install TextVault
```

## 🚀 Quick Start

```bash
# Create a new text file
tvault create notes

# Write content to the file
tvault write notes

# Read the file
tvault read notes

# Create a backup
tvault backup notes

# List all files
tvault list

# Get help
tvault --help
```

## 📖 Usage

### Basic Operations

| Command | Description | Example |
|---------|-------------|---------|
| `tvault create <file>` | Create a new text file | `tvault create notes` |
| `tvault read <file>` | Read content from a file | `tvault read notes` |
| `tvault write <file>` | Write content to a file (with backup) | `tvault write notes` |
| `tvault backup <file>` | Create a backup of a file | `tvault backup notes` |
| `tvault recover <file>` | Recover file from backup | `tvault recover notes` |
| `tvault remove <file>` | Remove a file | `tvault remove notes` |
| `tvault removebak <file>` | Remove backup file | `tvault removebak notes` |
| `tvault readbak <file>` | Read content from backup | `tvault readbak notes` |
| `tvault list` | List all files in vault | `tvault list` |
| `tvault backup-vault` | Backup entire vault | `tvault backup-vault` |
| `tvault remove-vault` | Remove vault and uninstall | `tvault remove-vault` |

### TOTP Feature

If a filename contains "tt" (e.g., `tt-pypi`), TVault can generate TOTP codes while reading:

```bash
# Create a file with TOTP secret
tvault create tt-pypi
tvault write tt-pypi  # Enter your TOTP secret key

# Read the file to get current TOTP code
tvault read tt-pypi
# Output: TOTP: 123456
```

### Advanced Options

```bash
# Force overwrite when creating files
tvault create existing-file --force

# Use custom data directory
tvault create notes --data-dir /path/to/custom/dir
```

## 🛠️ Development

### Project Structure

```
textvault/
├── tvault/
│   ├── __init__.py      # Package initialization
│   ├── tvault.py        # Main CLI logic
├── setup.py             # Installation configuration
├── README.md            # This file
└── LICENSE              # license
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
- **Issues**: [GitHub Issues](https://github.com/UniBinary/TextVault/issues)

## 🙏 Acknowledgments

- Thanks to all contributors and users
- Built with Python's standard library and [pyotp](https://github.com/pyauth/pyotp)

---

**Note**: This is version 1.1. The project is actively maintained and improved.