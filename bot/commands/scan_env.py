import discord
from discord.ext import commands
from discord import app_commands
from core.consent_manager import ConsentManager
from core.env_scanner import EnvScanner

class EnvScanCommand(commands.Cog):
    """Environment file scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = EnvScanner()
    
    @app_commands.command(name="scan_env", description="Scan for secrets in .env files")
    async def scan_env(self, interaction: discord.Interaction):
        """Scan for secrets in .env files"""
        user_id = interaction.user.id
        
        if not self.consent_mgr.has_consent(user_id, 'env') and not self.consent_mgr.has_consent(user_id, 'all'):
            await interaction.response.send_message("❌ You need to grant consent first! Use `/consent_env`", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            secrets = self.scanner.scan_env_files(start_path=None)
            
            report = f"""
📝 **ENVIRONMENT SCAN RESULTS**

Secrets Found: {len(secrets)}

**Exposed Secrets:**
```
{self._format_secrets(secrets)}
```

⚠️ These files contain critical secrets! Protect them!
            """
            
            if len(report) > 2000:
                await interaction.followup.send(report[:2000], ephemeral=True)
                await interaction.followup.send(report[2000:], ephemeral=True)
            else:
                await interaction.followup.send(report, ephemeral=True)
            
            self.consent_mgr.log_consent(user_id, 'env', True, f"Scan complete - {len(secrets)} secrets found")
        except Exception as e:
            await interaction.followup.send(f"❌ Error during scan: {str(e)}", ephemeral=True)
    
    def _format_secrets(self, secrets):
        """Format secrets for display"""
        if not secrets:
            return "None found"
        
        result = []
        for secret in secrets[:10]:  # Show first 10
            result.append(f"File: {secret.get('file', 'Unknown')}")
            result.append(f"Type: {secret.get('type', 'Unknown')}")
            result.append(f"Value: {secret.get('value', 'Unknown')}")
            result.append("---")
        
        return "\n".join(result)

async def setup(bot):
    await bot.add_cog(EnvScanCommand(bot))
