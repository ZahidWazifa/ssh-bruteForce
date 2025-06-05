# SSH Bruteforce Tool

A Python-based SSH bruteforce tool for security testing and penetration testing purposes.

## ⚠️ Disclaimer

This tool is intended for educational and authorized security testing purposes only. Only use this tool on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal and unethical.

## Features

- Multi-threaded SSH bruteforce attacks
- Customizable wordlists for usernames and passwords
- Detailed logging and reporting
- Support for custom credential combinations
- Rate limiting and timeout controls
- Progress tracking and status updates

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ssh-bruteforce-tool
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install the package:

```bash
pip install -e .
```

## Quick Start

```python
from src.ssh_bruteforce import SSHBruteforce

# Basic usage
bruteforcer = SSHBruteforce("192.168.1.100")
bruteforcer.run()
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Usage Instructions](docs/usage.md)
- [Configuration Options](docs/configuration.md)

## Contributing

Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
