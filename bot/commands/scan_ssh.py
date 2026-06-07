import discord
from discord.ext import commands
from core.consent_manager import ConsentManager
from core.ssh_scanner import SSHScanner

class SSHScanCommand(commands.Cog):
    """SSH key scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = SSHScanner()
    
    @commands.command(name='scan_ssh')
    async def scan_ssh(self, ctx):
        """Scan for SSH keys"""
        user_id = ctx.author.id
        
        if not self.consent_mgr.has_consent(user_id, 'all'):
            await ctx.author.send("❌ SSH scanning requires full audit consent! Use `!consent_all`")
            return
        
        await ctx.author.send("🔍 Scanning for SSH keys...")
        
        try:
            keys = self.scanner.scan_ssh_keys()
            
            report = f"""
🔑 **SSH KEY SCAN RESULTS**

SSH Keys Found: {len(keys)}

**Keys:**
```
{self._format_keys(keys)}
```

⚠️ SSH private keys should NEVER be exposed!
            """
            
            await ctx.author.send(report)
            self.consent_mgr.log_consent(user_id, 'ssh', True, f"Scan complete - {len(keys)} keys found")
        except Exception as e:
            await ctx.author.send(f"❌ Error during scan: {str(e)}")
    
    def _format_keys(self, keys):
        """Format SSH keys for display"""
        if not keys:
            return "None found"
        
        result = []
        for key in keys:
            result.append(f"File: {key.get('filename', 'Unknown')}")
            result.append(f"Private: {key.get('is_private', False)}")
            result.append(f"Size: {key.get('size', 0)} bytes")
            result.append("---")
        
        return "\n".join(result)

async def setup(bot):
    await bot.add_cog(SSHScanCommand(bot))
