# Custom Wordlists Directory

This directory is for storing custom wordlists that you create for specific targets or scenarios.

## Usage

You can create custom wordlists using the WordlistManager class:

```python
from src.utils.wordlist_manager import WordlistManager

wm = WordlistManager()
custom_users = ["admin", "administrator", "root", "user"]
wm.create_custom_wordlist(custom_users, "custom/my_users.txt")
```

## File Naming Convention

- `*_users.txt` - Username wordlists
- `*_passwords.txt` - Password wordlists
- `*_combined.txt` - Combined username:password format

## Examples

- `company_users.txt` - Company-specific usernames
- `weak_passwords.txt` - Common weak passwords
- `target_specific.txt` - Target-specific credentials
