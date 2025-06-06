# Installation Guide

This guide will walk you through installing and setting up the SSH Bruteforce Tool.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning repository)

## Installation Methods

### Method 1: Clone and Install

1. Clone the repository:

```bash
git clone <repository-url>
cd ssh-bruteforce-tool
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Install the package in development mode:

```bash
pip install -e .
```

### Method 2: Direct Installation

```bash
pip install -r requirements.txt
python setup.py install
```

## Verify Installation

Test that the installation was successful:

```bash
python -c "from src.ssh_bruteforce import SSHBruteforce; print('Installation successful!')"
```

## Dependencies

The tool requires the following Python packages:

- **paramiko** (>=2.11.0) - SSH client library
- **pycryptodome** (>=3.15.0) - Cryptographic library
- **colorama** (>=0.4.4) - Colored terminal output
- **tqdm** (>=4.64.0) - Progress bars
- **python-dateutil** (>=2.8.2) - Date utilities
- **pyyaml** (>=6.0) - YAML configuration files
- **argparse** (>=1.4.0) - Command line argument parsing

## Troubleshooting

### Common Issues

#### 1. paramiko Installation Issues

If you encounter issues installing paramiko on Windows:

```bash
pip install --upgrade pip
pip install paramiko --no-cache-dir
```

For Linux systems, you might need additional dependencies:

```bash
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```

#### 2. Permission Issues

On Linux/macOS, you might need to use `sudo` for system-wide installation:

```bash
sudo pip install -r requirements.txt
```

#### 3. Virtual Environment Issues

If virtual environment creation fails:

```bash
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv
```

### Testing Installation

Run the test suite to verify everything is working:

```bash
python -m pytest tests/ -v
```

### Development Installation

For development purposes:

1. Install in editable mode:

```bash
pip install -e .
```

2. Install development dependencies:

```bash
pip install pytest pytest-cov black flake8
```

## Configuration

After installation, you can:

1. Copy the example configuration:

```bash
cp config.example.yaml config.yaml
```

2. Edit the configuration file to match your needs

3. Test the configuration:

```bash
python -c "from src.config import Config; c = Config(); print('Config loaded successfully')"
```

## Uninstallation

To uninstall the tool:

```bash
pip uninstall ssh-bruteforce-tool
```

Clean up virtual environment:

```bash
deactivate
rm -rf venv
```

## Getting Help

If you encounter any issues during installation:

1. Check the troubleshooting section above
2. Ensure you have the correct Python version (3.8+)
3. Try installing in a fresh virtual environment
4. Check GitHub issues for similar problems
5. Create a new issue if the problem persists

## Next Steps

After successful installation, see:

- [Usage Guide](usage.md) - Learn how to use the tool
- [Configuration Guide](configuration.md) - Customize the tool settings
- [Examples](../examples/) - See practical usage examples
