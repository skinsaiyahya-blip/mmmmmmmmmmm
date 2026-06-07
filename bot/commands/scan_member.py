import discord
from discord.ext import commands
from discord import app_commands, ui
from core.consent_manager import ConsentManager

class MemberSelect(ui.Select):
    """Member selection dropdown"""
    
    def __init__(self, members):
        options = [
            discord.SelectOption(label=member.name, value=str(member.id))
            for member in members[:25]  # Discord limit
        ]
        super().__init__(placeholder="Select a member to scan...", options=options)
        self.selected_member = None
    
    async def callback(self, interaction: discord.Interaction):
        self.selected_member = int(self.values[0])
        await interaction.response.defer()

class MemberScanView(ui.View):
    """View with member selection"""
    
    def __init__(self, members):
        super().__init__()
        self.add_item(MemberSelect(members))
        self.member_select = self.children[0]

class MemberScanCommand(commands.Cog):
    """Member security scanning"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
    
    @app_commands.command(name="scan_member", description="Select a server member to scan (if they have bot installed)")
    async def scan_member(self, interaction: discord.Interaction):
        """Scan a member for vulnerabilities"""
        user_id = interaction.user.id
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message("❌ This command only works in servers", ephemeral=True)
            return
        
        # Get all members except bot
        members = [m for m in await guild.fetch_members(limit=None) if not m.bot]
        
        if not members:
            await interaction.response.send_message("❌ No members to scan", ephemeral=True)
            return
        
        view = MemberScanView(members)
        await interaction.response.send_message("📋 Select a member to scan:", view=view, ephemeral=True)
        
        # Wait for selection
        await view.wait()
        
        selected_id = view.member_select.selected_member
        if selected_id is None:
            await interaction.followup.send("❌ No member selected", ephemeral=True)
            return
        
        member = guild.get_member(selected_id)
        if not member:
            await interaction.followup.send("❌ Member not found", ephemeral=True)
            return
        
        # Log the scan request
        self.consent_mgr.log_consent(user_id, f'member_scan_{selected_id}', True, f"Scanned member: {member.name}")
        
        embed = discord.Embed(
            title=f"🔍 Scan Results for {member.name}",
            description=f"Member ID: {member.id}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="ℹ️ Info",
            value=f"Username: {member.name}\nJoined: {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'Unknown'}",
            inline=False
        )
        
        embed.add_field(
            name="🔐 Status",
            value="Waiting for member's bot scan...\n(Member must have bot installed locally to send results)",
            inline=False
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MemberScanCommand(bot))
