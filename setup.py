"""
Setup configuration for the Advanced Calculator package.

This module handles package metadata and dependencies for installation.
"""
from setuptools import setup, find_packages

# Read README for long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="advanced_calculator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    author="Software Engineering Student",
    author_email="student@university.edu",
    description="Advanced calculator with plugin system and history management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
