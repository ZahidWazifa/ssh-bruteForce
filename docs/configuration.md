# Configuration Guide

This guide explains how to configure the SSH Bruteforce Tool for optimal performance and customization.

## Configuration Overview

The tool uses a hierarchical configuration system with the following priority:

1. Command line arguments (highest priority)
2. Configuration file (config.yaml)
3. Default values (lowest priority)

## Configuration File Format

The configuration uses YAML format. Create a `config.yaml` file in the project root:

```yaml
ssh:
  default_port: 22
  timeout: 5
  max_retries: 3

bruteforce:
  max_threads: 10
  delay_between_attempts: 0.1
  stop_on_first_success: false

logging:
  log_level: "INFO"
  log_file: "logs/ssh_bruteforce.log"
  log_attempts: true
  log_successes: true
  log_errors: true

wordlists:
  default_userlist: "wordlists/common_users.txt"
  default_passlist: "wordlists/common_passwords.txt"
  default_creds: "wordlists/default_creds.txt"

output:
  save_results: true
  results_file: "logs/results.txt"
  verbose: true
```

## Configuration Sections

### SSH Settings

```yaml
ssh:
  default_port: 22 # Default SSH port
  timeout: 5 # Connection timeout in seconds
  max_retries: 3 # Maximum connection retries
```

**Parameters:**

- `default_port`: Default port for SSH connections
- `timeout`: How long to wait for SSH connection
- `max_retries`: Number of retry attempts for failed connections

### Bruteforce Settings

```yaml
bruteforce:
  max_threads: 10 # Maximum concurrent threads
  delay_between_attempts: 0.1 # Delay between attempts (seconds)
  stop_on_first_success: false # Stop after first successful login
```

**Parameters:**

- `max_threads`: Number of concurrent attack threads
- `delay_between_attempts`: Delay to prevent overwhelming target
- `stop_on_first_success`: Whether to stop after finding first valid credentials

### Logging Configuration

```yaml
logging:
  log_level: "INFO" # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/ssh_bruteforce.log" # Main log file
  log_attempts: true # Log all login attempts
  log_successes: true # Log successful logins
  log_errors: true # Log errors
```

**Log Levels:**

- `DEBUG`: Detailed debugging information
- `INFO`: General information messages
- `WARNING`: Warning messages
- `ERROR`: Error messages only

### Wordlist Configuration

```yaml
wordlists:
  default_userlist: "wordlists/common_users.txt"
  default_passlist: "wordlists/common_passwords.txt"
  default_creds: "wordlists/default_creds.txt"
```

**Parameters:**

- `default_userlist`: Default username wordlist file
- `default_passlist`: Default password wordlist file
- `default_creds`: Default credentials file (username:password format)

### Output Configuration

```yaml
output:
  save_results: true # Save results to file
  results_file: "logs/results.txt" # Results output file
  verbose: true # Verbose console output
```

## Using Configuration in Code

### Loading Configuration

```python
from src.config import Config

# Load configuration
config = Config()

# Load from specific file
config = Config("my_config.yaml")
```

### Accessing Configuration Values

```python
# Get values using dot notation
port = config.get('ssh.default_port', 22)
threads = config.get('bruteforce.max_threads', 10)
timeout = config.get('ssh.timeout', 5)

# Get nested configuration
ssh_config = config.get('ssh', {})
```

### Modifying Configuration

```python
# Set individual values
config.set('ssh.timeout', 10)
config.set('bruteforce.max_threads', 20)

# Save changes to file
config.save_config()
```

## Performance Tuning

### Thread Configuration

**Conservative (Low Resource Usage):**

```yaml
bruteforce:
  max_threads: 3
  delay_between_attempts: 0.5
```

**Balanced (Recommended):**

```yaml
bruteforce:
  max_threads: 10
  delay_between_attempts: 0.1
```

**Aggressive (High Performance):**

```yaml
bruteforce:
  max_threads: 20
  delay_between_attempts: 0.05
```

### Network Settings

**Slow/Unreliable Networks:**

```yaml
ssh:
  timeout: 15
  max_retries: 5

bruteforce:
  max_threads: 5
  delay_between_attempts: 0.3
```

**Fast Local Networks:**

```yaml
ssh:
  timeout: 2
  max_retries: 2

bruteforce:
  max_threads: 15
  delay_between_attempts: 0.05
```

## Environment-Specific Configurations

### Development Environment

```yaml
# dev_config.yaml
ssh:
  timeout: 1

bruteforce:
  max_threads: 3
  delay_between_attempts: 0.1
  stop_on_first_success: true

logging:
  log_level: "DEBUG"
  verbose: true
```

### Production Environment

```yaml
# prod_config.yaml
ssh:
  timeout: 5
  max_retries: 3

bruteforce:
  max_threads: 10
  delay_between_attempts: 0.2

logging:
  log_level: "INFO"
  log_attempts: true
  log_successes: true
```

### Penetration Testing

```yaml
# pentest_config.yaml
ssh:
  timeout: 3

bruteforce:
  max_threads: 8
  delay_between_attempts: 0.1
  stop_on_first_success: false

wordlists:
  default_userlist: "wordlists/custom/target_users.txt"
  default_passlist: "wordlists/custom/target_passwords.txt"

output:
  save_results: true
  results_file: "logs/pentest_results.txt"
```

## Advanced Configuration

### Custom Wordlist Paths

```yaml
wordlists:
  custom_paths:
    - "/path/to/custom/wordlists"
    - "~/security/wordlists"

  username_files:
    - "common_users.txt"
    - "custom/target_users.txt"
    - "custom/admin_users.txt"

  password_files:
    - "common_passwords.txt"
    - "custom/weak_passwords.txt"
    - "custom/company_passwords.txt"
```

### Target-Specific Settings

```yaml
targets:
  "192.168.1.100":
    port: 2222
    timeout: 10
    threads: 5

  "production.company.com":
    port: 22
    timeout: 15
    threads: 3
    delay: 0.5
```

### Rate Limiting

```yaml
rate_limiting:
  enabled: true
  requests_per_minute: 100
  burst_limit: 20
  backoff_factor: 1.5
```

## Configuration Validation

### Automatic Validation

```python
from src.config import Config

config = Config()

# Validate configuration
if config.validate_config():
    print("Configuration is valid")
else:
    print("Configuration has errors")
```

### Manual Validation

```python
# Check required values
required_settings = [
    'ssh.timeout',
    'bruteforce.max_threads',
    'logging.log_file'
]

for setting in required_settings:
    value = config.get(setting)
    if value is None:
        print(f"Missing required setting: {setting}")
```

## Configuration Examples

### Example 1: High-Speed Local Network

```yaml
# local_fast.yaml
ssh:
  timeout: 1
  max_retries: 2

bruteforce:
  max_threads: 25
  delay_between_attempts: 0.01

logging:
  log_level: "WARNING" # Reduce log verbosity
```

### Example 2: Careful Remote Testing

```yaml
# remote_careful.yaml
ssh:
  timeout: 10
  max_retries: 3

bruteforce:
  max_threads: 3
  delay_between_attempts: 1.0
  stop_on_first_success: true

logging:
  log_level: "INFO"
  log_attempts: true
```

### Example 3: Comprehensive Testing

```yaml
# comprehensive.yaml
ssh:
  timeout: 5

bruteforce:
  max_threads: 12
  delay_between_attempts: 0.15

wordlists:
  default_userlist: "wordlists/comprehensive_users.txt"
  default_passlist: "wordlists/comprehensive_passwords.txt"

output:
  save_results: true
  results_file: "logs/comprehensive_results.txt"
  verbose: true
```

## Troubleshooting Configuration

### Common Issues

**Configuration file not found:**

- Ensure `config.yaml` exists in project root
- Check file permissions
- Verify YAML syntax

**Invalid YAML syntax:**

- Use online YAML validators
- Check indentation (use spaces, not tabs)
- Verify quotes and colons

**Values not taking effect:**

- Check configuration priority order
- Verify dot notation syntax
- Ensure proper data types

### Debug Configuration

```python
from src.config import Config

config = Config()

# Print all configuration
import json
print(json.dumps(config.get_all(), indent=2))

# Check specific values
print(f"SSH timeout: {config.get('ssh.timeout')}")
print(f"Max threads: {config.get('bruteforce.max_threads')}")
```

## Security Considerations

### Protecting Configuration Files

- Don't commit sensitive configurations to version control
- Use environment variables for sensitive values
- Set appropriate file permissions (600)

### Configuration Templates

Create template files for different scenarios:

```bash
# Copy appropriate template
cp configs/pentest_template.yaml config.yaml

# Customize for your needs
nano config.yaml
```

## Best Practices

1. **Start with defaults** - Use default configuration initially
2. **Test changes** - Validate configuration changes in safe environment
3. **Document customizations** - Keep notes on why settings were changed
4. **Version control** - Track configuration changes
5. **Environment separation** - Use different configs for different environments

## Configuration Schema

For reference, here's the complete configuration schema:

```yaml
ssh:
  default_port: integer (1-65535)
  timeout: integer (1-300)
  max_retries: integer (1-10)

bruteforce:
  max_threads: integer (1-100)
  delay_between_attempts: float (0.0-10.0)
  stop_on_first_success: boolean

logging:
  log_level: string (DEBUG|INFO|WARNING|ERROR)
  log_file: string (file path)
  log_attempts: boolean
  log_successes: boolean
  log_errors: boolean

wordlists:
  default_userlist: string (file path)
  default_passlist: string (file path)
  default_creds: string (file path)

output:
  save_results: boolean
  results_file: string (file path)
  verbose: boolean
```
