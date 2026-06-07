import os
from dotenv import load_dotenv

load_dotenv()

# Bot token from Discord Developer Portal
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Your personal Discord ID (only YOU will receive the data)
OWNER_DISCORD_ID = int(os.getenv("OWNER_DISCORD_ID", "0"))

# Log file for accountability
LOG_FILE = "consent_log.txt"

# Only allow commands in specific servers/channels (security)
ALLOWED_GUILD_IDS = [int(os.getenv("ALLOWED_GUILD_ID", "0"))]

# Database file
CONSENT_DB_FILE = "data/consent.db"

# Logging
LOG_DIR = "data/logs"
LOG_LEVEL = "INFO"
