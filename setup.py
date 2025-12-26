#!/usr/bin/env python3
"""
Setup script para OpenVPN Manager CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer el README para la descripción larga
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="openvpn-manager-cli",
    version="1.0.0",
    author="Daniel Puentes",
    author_email="Contact@Electrobridges.com",
    description="Una aplicación CLI moderna e interactiva para gestionar servidores OpenVPN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Electrobridges/OpenVPN-Manager-CLI",
    project_urls={
        "Bug Reports": "https://github.com/Electrobridges/OpenVPN-Manager-CLI/issues",
        "Source": "https://github.com/Electrobridges/OpenVPN-Manager-CLI",
        "Documentation": "https://github.com/Electrobridges/OpenVPN-Manager-CLI/blob/main/docs/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ovpn-manager=ovpn-manager:main",
        ],
    },
    keywords="openvpn, vpn, management, cli, terminal, sysadmin",
    include_package_data=True,
    zip_safe=False,
)
