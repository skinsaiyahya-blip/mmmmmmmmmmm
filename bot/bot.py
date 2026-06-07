import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN

class EthicalSecurityBot(commands.Cog):
    """Main bot cog"""
    
    def __init__(self, bot):
        self.bot = bot

def create_bot():
    """Create and configure bot"""
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot

def load_cogs(bot):
    """Load all command cogs"""
    # Commands will be loaded dynamically
    pass
