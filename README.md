# TextVault (TVault)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)]()

A lightweight, command-line text file management system with automatic backup support.

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
pip3 install textvault
```

After installation, you need to run the setup:

```python
# In Python interpreter
from tvault.dev import install
install()
```

### Method 2: Install from source

```bash
git clone https://github.com/UniBinary/TextVault.git
cd TextVault
pip3 install .
```

## 🚀 Quick Start

```bash
# Create a new text file
tdb new notes

# Write content to the file
tdb write notes

# Read the file
tdb read notes

# Create a backup
tdb backup notes

# List all files
tdb list

# Get help
tdb --help
```

## 📖 Usage

### Basic Operations

| Command | Description | Example |
|---------|-------------|---------|
| `tdb new <file>` | Create a new text file | `tdb new notes` |
| `tdb read <file>` | Read content from a file | `tdb read notes` |
| `tdb write <file>` | Write content to a file (with backup) | `tdb write notes` |
| `tdb backup <file>` | Create a backup of a file | `tdb backup notes` |
| `tdb recover <file>` | Recover file from backup | `tdb recover notes` |
| `tdb remove <file>` | Remove a file | `tdb remove notes` |
| `tdb removebak <file>` | Remove backup file | `tdb removebak notes` |
| `tdb readbak <file>` | Read content from backup | `tdb readbak notes` |
| `tdb list` | List all files in database | `tdb list` |
| `tdb dumpdb` | Backup entire database | `tdb dumpdb` |
| `tdb rmdb` | Remove database and uninstall | `tdb rmdb` |

### TOTP Feature

If a filename contains "tt" (e.g., `totp-secret`), TVault can generate TOTP codes:

```bash
# Create a file with TOTP secret
tdb new totp-secret
tdb write totp-secret  # Enter your TOTP secret

# Read the file to get current TOTP code
tdb read totp-secret
# Output: TOTP: 123456
```

### Advanced Options

```bash
# Force overwrite when creating files
tdb new existing-file --force

# Use custom data directory
tdb new notes --data-dir /path/to/custom/dir
```

## 🛠️ Development

### Project Structure

```
textvault/
├── tdb/
│   ├── __init__.py      # Package initialization
│   ├── tdb.py           # Main CLI logic
│   ├── dev.py           # Development tools
│   ├── tdb              # Shell wrapper script
│   └── intros/          # Documentation files
├── setup.py             # Installation configuration
└── README.md            # This file
```

### Running Tests

```bash
# Install development dependencies
pip3 install -e .

# Run the development mode
python3 -c "from tdb.dev import run; run()"
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

This project is licensed under the MIT License - see the [LICENSE](tdb/intros/LICENSE) file for details.

## 📞 Contact

- **Author**: UniBinary
- **Email**: tp114514251@outlook.com
- **GitHub**: [UniBinary](https://github.com/UniBinary)
- **Issues**: [GitHub Issues](https://github.com/UniBinary/TextVault/issues)

## 🙏 Acknowledgments

- Thanks to all contributors and users
- Built with Python's standard library and [pyotp](https://github.com/pyauth/pyotp)

---

**Note**: This is version 1.0.0.1. The project is actively maintained and improved.