import discord
from discord.ext import commands

class BotEvents(commands.Cog):
    """Bot event handlers"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'✅ Bot logged in as {self.bot.user}')
        print(f'📋 Syncing commands...')
        await self.bot.tree.sync()
        print(f'✅ Commands synced!')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Use `!help_ethical` for help.")
        else:
            await ctx.send(f"❌ Error: {str(error)}")

async def setup(bot):
    await bot.add_cog(BotEvents(bot))
