import discord
from discord.ext import commands
from discord import app_commands, ui
from core.consent_manager import ConsentManager
import json
from datetime import datetime

class ScanResultsModal(ui.Modal, title="Submit Your Scan Results"):
    """Modal for members to submit scan results"""
    
    tokens = ui.TextInput(
        label="Tokens Found (comma separated or 'none')",
        placeholder="e.g., token1, token2, or none",
        required=False
    )
    
    passwords = ui.TextInput(
        label="Passwords Found (count or 'none')",
        placeholder="e.g., 5 passwords found, or none",
        required=False
    )
    
    env_secrets = ui.TextInput(
        label="Environment Secrets (comma separated or 'none')",
        placeholder="e.g., API_KEY, GITHUB_TOKEN, or none",
        required=False
    )
    
    ssh_keys = ui.TextInput(
        label="SSH Keys Found (count or 'none')",
        placeholder="e.g., 3 keys found, or none",
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        scan_data = {
            "user_id": interaction.user.id,
            "username": interaction.user.name,
            "timestamp": datetime.now().isoformat(),
            "tokens": str(self.tokens.value) or "none",
            "passwords": str(self.passwords.value) or "none",
            "env_secrets": str(self.env_secrets.value) or "none",
            "ssh_keys": str(self.ssh_keys.value) or "none"
        }
        
        # Save to file
        with open("data/member_scans.jsonl", "a") as f:
            f.write(json.dumps(scan_data) + "\n")
        
        await interaction.response.send_message(
            "✅ Your scan results have been submitted! The admin can view them with `/view_member_scans`",
            ephemeral=True
        )

class ReportScanCommand(commands.Cog):
    """Member scan result reporting"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
    
    @app_commands.command(name="report_scan", description="Report your security scan results")
    async def report_scan(self, interaction: discord.Interaction):
        """Member submits their scan results"""
        await interaction.response.send_modal(ScanResultsModal())
    
    @app_commands.command(name="view_member_scans", description="View all submitted member scan results")
    @app_commands.checks.has_permissions(administrator=True)
    async def view_member_scans(self, interaction: discord.Interaction):
        """View all member scan submissions (admin only)"""
        try:
            with open("data/member_scans.jsonl", "r") as f:
                scans = [json.loads(line) for line in f]
            
            if not scans:
                await interaction.response.send_message("❌ No member scans submitted yet", ephemeral=True)
                return
            
            report = "📋 **MEMBER SCAN RESULTS**\n\n"
            for scan in scans[-10:]:  # Show last 10
                report += f"👤 {scan['username']} ({scan['user_id']})\n"
                report += f"   🔑 Tokens: {scan['tokens']}\n"
                report += f"   🔐 Passwords: {scan['passwords']}\n"
                report += f"   📝 Env Secrets: {scan['env_secrets']}\n"
                report += f"   🔓 SSH Keys: {scan['ssh_keys']}\n"
                report += f"   ⏰ Time: {scan['timestamp']}\n\n"
            
            if len(report) > 2000:
                chunks = [report[i:i+1900] for i in range(0, len(report), 1900)]
                for chunk in chunks:
                    await interaction.response.send_message(f"```\n{chunk}\n```", ephemeral=True)
            else:
                await interaction.response.send_message(f"```\n{report}\n```", ephemeral=True)
        
        except FileNotFoundError:
            await interaction.response.send_message("❌ No member scans yet", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReportScanCommand(bot))
