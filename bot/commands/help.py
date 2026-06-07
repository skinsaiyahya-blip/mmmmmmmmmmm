import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    """Help and information commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help_ethical", description="Show all available commands")
    async def help_ethical(self, interaction: discord.Interaction):
        """Show all available commands"""
        embed = discord.Embed(
            title="🛡️ Ethical Security Bot - Commands",
            description="All commands require explicit consent and are for self-auditing only!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📋 Consent Management",
            value="""
`/consent_tokens` - Ask for token scanning consent
`/consent_passwords` - Ask for password scanning consent
`/consent_env` - Ask for .env scanning consent
`/consent_all` - Ask for all scan consents
`/revoke_consent` - Revoke all granted consents
            """,
            inline=False
        )
        
        embed.add_field(
            name="🔍 Security Scans",
            value="""
`/scan_tokens` - Scan for exposed Discord/API tokens
`/scan_passwords` - Scan for saved browser passwords
`/scan_env` - Scan for secrets in .env files
`/scan_ssh` - Scan for SSH keys
`/scan_all` - Run full security audit (requires all consents)
            """,
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Important",
            value="""
✅ Always grant consent before scanning
✅ Results are sent ONLY to you via DM
✅ All actions are logged for accountability
❌ Never share tokens or passwords
❌ Only use on machines you own
            """,
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
