#!/usr/bin/env python3
"""
🛡️ Ethical Security Bot - Main Entry Point

A Discord bot for ethical security auditing with explicit user consent.
Every action is logged for accountability.

Usage:
    python main.py
"""

import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import logging
from config import DISCORD_BOT_TOKEN, OWNER_DISCORD_ID
from utils.logger import logger
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create bot with slash commands (no prefix needed)
intents = discord.Intents.default()
intents.message_content = False
intents.members = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Bot is ready"""
    logger.info(f"✅ Bot logged in as {bot.user}")
    logger.info(f"📋 Syncing commands...")
    try:
        await bot.tree.sync()
        logger.info(f"✅ Commands synced!")
    except Exception as e:
        logger.error(f"❌ Error syncing commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help_ethical` for help.")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"❌ Error: {str(error)}")

async def load_cogs():
    """Load all cogs"""
    cogs_list = [
        "bot.commands.help",
        "bot.commands.consent",
        "bot.commands.scan_tokens",
        "bot.commands.scan_passwords",
        "bot.commands.scan_env",
        "bot.commands.scan_ssh",
        "bot.commands.scan_member",
        "bot.commands.report_scan",
        "bot.commands.scan_all",
        "bot.events",
    ]
    
    for cog in cogs_list:
        try:
            await bot.load_extension(cog)
            logger.info(f"✅ Loaded {cog}")
        except Exception as e:
            logger.error(f"❌ Failed to load {cog}: {e}")

async def main():
    """Main function"""
    print("""
    ╔════════════════════════════════════════╗
    ║  🛡️  ETHICAL SECURITY BOT  🛡️        ║
    ║  Explicit Consent • Self-Audit Only   ║
    ╚════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Starting bot...")
    
    if not DISCORD_BOT_TOKEN or DISCORD_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ DISCORD_BOT_TOKEN not configured in .env!")
        return
    
    if not OWNER_DISCORD_ID or OWNER_DISCORD_ID == 0:
        logger.error("❌ OWNER_DISCORD_ID not configured in .env!")
        return
    
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
