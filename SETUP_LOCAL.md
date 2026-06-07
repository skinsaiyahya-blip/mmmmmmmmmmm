# 🚀 Run Bot Locally (Recommended for Full Scanning)

To scan your actual machine for tokens, passwords, SSH keys, and secrets, run the bot **locally** on your computer instead of Railway.

## Setup

### 1. Install Python 3.11+
- Download from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

### 2. Clone Repository
```bash
git clone https://github.com/skinsaiyahya-blip/mmmmmmmmmmm.git
cd mmmmmmmmmmm
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Bot Token
Create `.env` file in the project root:
```
DISCORD_BOT_TOKEN=your_bot_token_here
OWNER_DISCORD_ID=your_discord_id_here
ALLOWED_GUILD_ID=your_server_id_here
```

Get these from:
- **Bot Token**: https://discord.com/developers/applications → Select app → Copy token
- **Your ID**: Discord → Settings → Advanced → Developer Mode ON → Right-click yourself → Copy User ID
- **Server ID**: Right-click server → Copy Server ID

### 5. Run Locally
```bash
python main.py
```

Bot will be online whenever your PC is running!

## How It Works

### You (Admin)
- Run bot on your machine
- Commands like `/scan_tokens`, `/scan_passwords` work on YOUR machine
- You can use `/scan_member` to request scans from others
- You see admin command `/view_member_scans`

### Other Members
- Use `/report_scan` to submit their scan results
- No bot installation needed - just fill out a form
- Results stored and you (admin) can view with `/view_member_scans`

## Commands When Running Locally

**Self Scans:**
- `/scan_tokens` - Find Discord tokens in your system
- `/scan_passwords` - Find saved Chrome passwords
- `/scan_env` - Find secrets in .env files
- `/scan_ssh` - Find SSH keys
- `/scan_all` - Run full audit

**Member Scans:**
- `/scan_member` - Select member to request scan
- `/report_scan` - (For members) Submit your scan results
- `/view_member_scans` - (Admin) View all member submissions

**Consent:**
- `/consent_*` - Grant consent before scanning
- `/revoke_consent` - Revoke all consents

## Safety Notes

✅ Bot runs only on YOUR computer  
✅ You have full control over scans  
✅ No data leaves your machine unless YOU choose to share  
✅ All scans logged for accountability  
❌ Never share your `.env` file or bot token!

## Troubleshooting

**"Python not found"**
- Restart terminal after installing Python
- Make sure "Add Python to PATH" was checked

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Token invalid"**
- Check Discord Developer Portal for correct token
- Make sure bot has MESSAGE_CONTENT intent enabled

**Want to keep using Railway?**
- Railway version works for member scanning via `/report_scan`
- But can't scan the Railway server itself (only Railway's disk, not your machine)
- Best for keeping bot always online for member submissions
