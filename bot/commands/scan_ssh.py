import discord
from discord.ext import commands
from discord import app_commands
from core.consent_manager import ConsentManager
from core.ssh_scanner import SSHScanner

class SSHScanCommand(commands.Cog):
    """SSH key scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = SSHScanner()
    
    @app_commands.command(name="scan_ssh", description="Scan for SSH keys")
    async def scan_ssh(self, interaction: discord.Interaction):
        """Scan for SSH keys"""
        user_id = interaction.user.id
        
        if not self.consent_mgr.has_consent(user_id, 'all'):
            await interaction.response.send_message("❌ SSH scanning requires full audit consent! Use `/consent_all`", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
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
            
            if len(report) > 2000:
                await interaction.followup.send(report[:2000], ephemeral=True)
                await interaction.followup.send(report[2000:], ephemeral=True)
            else:
                await interaction.followup.send(report, ephemeral=True)
            
            self.consent_mgr.log_consent(user_id, 'ssh', True, f"Scan complete - {len(keys)} keys found")
        except Exception as e:
            await interaction.followup.send(f"❌ Error during scan: {str(e)}", ephemeral=True)
    
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
