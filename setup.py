#!/usr/bin/env python3
"""
Setup configuration for UniBinaryTextVault
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="UniBinaryTextVault",
    version="1.1",
    author="UniBinary",
    author_email="tp114514251@outlook.com",
    description="A lightweight text file management system for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UniBinary/TextVault",
    packages=find_packages(),
    package_data={
        "tvault": ["tvault", "intros/*", "intros/README.md", "intros/LICENSE"]
    },
    entry_points={
        "console_scripts": [
            "tvault=tvault.tvault:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],
    install_requires=[
        "pyotp>=2.6.0",
    ],
    python_requires=">=3.7",
    keywords="text, vault, file, management, backup, cli, secure",
    project_urls={
        "Bug Reports": "https://github.com/UniBinary/TextVault/issues",
        "Source": "https://github.com/UniBinary/TextVault",
        "PyPI": "https://pypi.org/project/UniBinaryTextVault/",
    },
)