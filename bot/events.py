import discord
from discord.ext import commands
from discord import app_commands
from utils.logger import logger

class BotEvents(commands.Cog):
    """Bot event handlers"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'✅ Bot logged in as {self.bot.user}')
        print(f'📋 Syncing commands...')
        await self.bot.tree.sync()
        print(f'✅ Slash commands synced!')
    
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"❌ Error in {interaction.command.name}: {error}")
        await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotEvents(bot))
