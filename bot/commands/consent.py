import discord
from discord.ext import commands
from discord import app_commands, ui
from core.consent_manager import ConsentManager

class ConfirmView(ui.View):
    """Reusable confirmation view with YES/NO buttons"""
    
    def __init__(self, timeout=60.0):
        super().__init__(timeout=timeout)
        self.result = None
    
    @ui.button(label="YES", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: ui.Button):
        self.result = True
        self.stop()
        await interaction.response.defer()
    
    @ui.button(label="NO", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: ui.Button):
        self.result = False
        self.stop()
        await interaction.response.defer()

class ConsentCommands(commands.Cog):
    """Consent management commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
    
    @app_commands.command(name="consent_tokens", description="Request consent to scan for Discord/API tokens")
    async def consent_tokens(self, interaction: discord.Interaction):
        """Request consent to scan for tokens"""
        user_id = interaction.user.id
        
        embed = discord.Embed(
            title="🔐 Token Scan Consent Request",
            description="Do you want to allow scanning for Discord/API tokens on this machine?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ What this will do:",
            value="Scan Discord leveldb storage and environment variables for tokens",
            inline=False
        )
        embed.add_field(
            name="📊 Click YES or NO:",
            value="Your response will determine if scanning is allowed",
            inline=False
        )
        
        view = ConfirmView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        await view.wait()
        
        if view.result is None:
            await interaction.followup.send("⏱️ Consent request timed out", ephemeral=True)
        elif view.result:
            self.consent_mgr.log_consent(user_id, 'tokens', True)
            await interaction.followup.send("✅ Token scanning consent granted!", ephemeral=True)
        else:
            self.consent_mgr.log_consent(user_id, 'tokens', False)
            await interaction.followup.send("❌ Token scanning consent denied", ephemeral=True)
    
    @app_commands.command(name="consent_passwords", description="Request consent to scan for saved browser passwords")
    async def consent_passwords(self, interaction: discord.Interaction):
        """Request consent to scan for passwords"""
        user_id = interaction.user.id
        
        embed = discord.Embed(
            title="🔐 Password Scan Consent Request",
            description="Do you want to allow scanning for saved browser passwords?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ What this will do:",
            value="Access Chrome/Firefox password database and decrypt saved passwords",
            inline=False
        )
        embed.add_field(
            name="📊 Click YES or NO:",
            value="Your response will determine if scanning is allowed",
            inline=False
        )
        
        view = ConfirmView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        await view.wait()
        
        if view.result is None:
            await interaction.followup.send("⏱️ Consent request timed out", ephemeral=True)
        elif view.result:
            self.consent_mgr.log_consent(user_id, 'passwords', True)
            await interaction.followup.send("✅ Password scanning consent granted!", ephemeral=True)
        else:
            self.consent_mgr.log_consent(user_id, 'passwords', False)
            await interaction.followup.send("❌ Password scanning consent denied", ephemeral=True)
    
    @app_commands.command(name="consent_env", description="Request consent to scan for secrets in .env files")
    async def consent_env(self, interaction: discord.Interaction):
        """Request consent to scan .env files"""
        user_id = interaction.user.id
        
        embed = discord.Embed(
            title="🔐 Environment Scan Consent Request",
            description="Do you want to allow scanning for secrets in .env files?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ What this will do:",
            value="Search for .env, .env.local files containing API keys, tokens, and secrets",
            inline=False
        )
        embed.add_field(
            name="📊 Click YES or NO:",
            value="Your response will determine if scanning is allowed",
            inline=False
        )
        
        view = ConfirmView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        await view.wait()
        
        if view.result is None:
            await interaction.followup.send("⏱️ Consent request timed out", ephemeral=True)
        elif view.result:
            self.consent_mgr.log_consent(user_id, 'env', True)
            await interaction.followup.send("✅ Environment scanning consent granted!", ephemeral=True)
        else:
            self.consent_mgr.log_consent(user_id, 'env', False)
            await interaction.followup.send("❌ Environment scanning consent denied", ephemeral=True)
    
    @app_commands.command(name="consent_all", description="Request consent for ALL security scans")
    async def consent_all(self, interaction: discord.Interaction):
        """Request consent for all scans"""
        user_id = interaction.user.id
        
        embed = discord.Embed(
            title="🔐 Full Audit Consent Request",
            description="Do you want to allow a FULL SECURITY AUDIT of your machine?",
            color=discord.Color.red()
        )
        embed.add_field(
            name="⚠️ This will scan for:",
            value="""
🔑 Discord/API tokens
🔐 Saved browser passwords
📝 .env files with secrets
🔓 SSH keys
🍪 Browser cookies
            """,
            inline=False
        )
        embed.add_field(
            name="📊 Click YES or NO:",
            value="Your response will determine if full audit is allowed",
            inline=False
        )
        
        view = ConfirmView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        await view.wait()
        
        if view.result is None:
            await interaction.followup.send("⏱️ Consent request timed out", ephemeral=True)
        elif view.result:
            self.consent_mgr.log_consent(user_id, 'all', True, "Full audit consent granted")
            await interaction.followup.send("✅ Full audit consent granted!", ephemeral=True)
        else:
            self.consent_mgr.log_consent(user_id, 'all', False)
            await interaction.followup.send("❌ Full audit consent denied", ephemeral=True)
    
    @app_commands.command(name="revoke_consent", description="Revoke all granted consents")
    async def revoke_consent(self, interaction: discord.Interaction):
        """Revoke all consents"""
        user_id = interaction.user.id
        self.consent_mgr.revoke_all_consent(user_id)
        await interaction.response.send_message("✅ All consents have been revoked!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ConsentCommands(bot))
