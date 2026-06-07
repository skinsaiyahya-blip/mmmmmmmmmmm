# 🛡️ Ethical Security Bot

A Discord bot that helps you audit YOUR OWN machine for security vulnerabilities. Every action requires explicit user consent and is logged for accountability.

## ⚠️ EDUCATIONAL & ETHICAL USE ONLY

This bot is designed to:
- Show you what an attacker would see on YOUR machine
- Help you identify and fix security issues
- Educate you about security best practices
- **Never** access anyone else's data without explicit, informed consent

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Configure
Create a `.env` file:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
OWNER_DISCORD_ID=123456789012345678
ALLOWED_GUILD_ID=987654321098765432
```

Get your bot token: https://discord.com/developers/applications

### 3. Run
```bash
python main.py
```

## 📋 Available Commands

- `!help_ethical` - Show all commands
- `!consent_tokens` - Request consent to scan Discord tokens
- `!scan_tokens` - Scan for Discord tokens
- `!consent_passwords` - Request consent to scan browser passwords
- `!scan_passwords` - Scan saved browser passwords
- `!consent_env` - Request consent to scan .env files
- `!scan_env` - Scan for exposed secrets
- `!consent_all` - Grant consent for all scans
- `!scan_all` - Run full security audit
- `!revoke_consent` - Revoke all consents

## 🔐 Security Features

✅ **Explicit Consent** - Every scan requires user consent first
✅ **Audit Logging** - All actions logged to `consent_log.txt`
✅ **Data Privacy** - Results only sent to the user via DM
✅ **Self-Only** - Can only scan the machine it's running on
✅ **Educational** - Shows what attackers would target

## 📁 Project Structure

```
EthicalSecurityBot/
├── .env                 # Configuration (secrets)
├── .gitignore
├── requirements.txt
├── README.md
├── main.py              # Entry point
├── config.py            # Configuration loader
├── bot/                 # Discord bot package
│   ├── bot.py
│   ├── events.py
│   └── commands/
├── core/                # Scanning engines
│   ├── consent_manager.py
│   ├── token_scanner.py
│   ├── password_scanner.py
│   ├── env_scanner.py
│   ├── ssh_scanner.py
│   ├── cookie_scanner.py
│   └── reporter.py
├── utils/               # Helper utilities
│   ├── file_utils.py
│   ├── crypto_utils.py
│   ├── path_utils.py
│   └── logger.py
├── tests/               # Unit tests
├── data/                # Runtime data (auto-created)
└── backups/             # Backups (auto-created)
```

## 📝 Logging & Accountability

Every action is logged to `consent_log.txt`:
```
[2024-01-15T10:30:45] USER:123456789 ACTION:tokens DETAILS:CONSENT_GRANTED
[2024-01-15T10:30:50] USER:123456789 ACTION:tokens DETAILS:SCAN_COMPLETE
```

## 🤝 Contributing

This is an educational tool. Feel free to fork and improve it!

## ⚖️ Legal

**Use this tool ONLY on machines you own or have explicit permission to audit.**

Unauthorized access to someone else's data is illegal.

## 📚 Learning Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Windows Security Best Practices](https://learn.microsoft.com/en-us/windows/security/)

---

**Remember: With great power comes great responsibility. Use ethically.** 🛡️
