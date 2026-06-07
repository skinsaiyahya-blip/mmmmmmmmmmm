import discord
from discord.ext import commands
from core.consent_manager import ConsentManager

class ConsentCommands(commands.Cog):
    """Consent management commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.consent_mgr = ConsentManager()
    
    @commands.command(name='consent_tokens')
    async def consent_tokens(self, ctx):
        """Request consent to scan for tokens"""
        user_id = ctx.author.id
        
        embed = discord.Embed(
            title="🔐 Token Scan Consent Request",
            description="Do you want to allow scanning for Discord/API tokens on this machine?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ What this will do:",
            value="Scan Discord leveldb storage and environment variables for tokens",
            inline=False
        )
        embed.add_field(
            name="📊 Reply with:",
            value="`YES` to grant consent\n`NO` to deny",
            inline=False
        )
        
        await ctx.author.send(embed=embed)
        
        def check(m):
            return m.author.id == user_id and m.content.upper() in ['YES', 'NO']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.upper() == 'YES':
                self.consent_mgr.log_consent(user_id, 'tokens', True)
                await ctx.author.send("✅ Token scanning consent granted!")
            else:
                self.consent_mgr.log_consent(user_id, 'tokens', False)
                await ctx.author.send("❌ Token scanning consent denied")
        except:
            await ctx.author.send("⏱️ Consent request timed out")
    
    @commands.command(name='consent_passwords')
    async def consent_passwords(self, ctx):
        """Request consent to scan for passwords"""
        user_id = ctx.author.id
        
        embed = discord.Embed(
            title="🔐 Password Scan Consent Request",
            description="Do you want to allow scanning for saved browser passwords?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ What this will do:",
            value="Access Chrome/Firefox password database and decrypt saved passwords",
            inline=False
        )
        embed.add_field(
            name="📊 Reply with:",
            value="`YES` to grant consent\n`NO` to deny",
            inline=False
        )
        
        await ctx.author.send(embed=embed)
        
        def check(m):
            return m.author.id == user_id and m.content.upper() in ['YES', 'NO']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.upper() == 'YES':
                self.consent_mgr.log_consent(user_id, 'passwords', True)
                await ctx.author.send("✅ Password scanning consent granted!")
            else:
                self.consent_mgr.log_consent(user_id, 'passwords', False)
                await ctx.author.send("❌ Password scanning consent denied")
        except:
            await ctx.author.send("⏱️ Consent request timed out")
    
    @commands.command(name='consent_env')
    async def consent_env(self, ctx):
        """Request consent to scan .env files"""
        user_id = ctx.author.id
        
        embed = discord.Embed(
            title="🔐 Environment Scan Consent Request",
            description="Do you want to allow scanning for secrets in .env files?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ What this will do:",
            value="Search for .env, .env.local files containing API keys, tokens, and secrets",
            inline=False
        )
        embed.add_field(
            name="📊 Reply with:",
            value="`YES` to grant consent\n`NO` to deny",
            inline=False
        )
        
        await ctx.author.send(embed=embed)
        
        def check(m):
            return m.author.id == user_id and m.content.upper() in ['YES', 'NO']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.upper() == 'YES':
                self.consent_mgr.log_consent(user_id, 'env', True)
                await ctx.author.send("✅ Environment scanning consent granted!")
            else:
                self.consent_mgr.log_consent(user_id, 'env', False)
                await ctx.author.send("❌ Environment scanning consent denied")
        except:
            await ctx.author.send("⏱️ Consent request timed out")
    
    @commands.command(name='consent_all')
    async def consent_all(self, ctx):
        """Request consent for all scans"""
        user_id = ctx.author.id
        
        embed = discord.Embed(
            title="🔐 Full Audit Consent Request",
            description="Do you want to allow a FULL SECURITY AUDIT of your machine?",
            color=discord.Color.red()
        )
        embed.add_field(
            name="⚠️ This will scan for:",
            value="""
🔑 Discord/API tokens
🔐 Saved browser passwords
📝 .env files with secrets
🔓 SSH keys
🍪 Browser cookies
            """,
            inline=False
        )
        embed.add_field(
            name="📊 Reply with:",
            value="`YES` to grant consent\n`NO` to deny",
            inline=False
        )
        
        await ctx.author.send(embed=embed)
        
        def check(m):
            return m.author.id == user_id and m.content.upper() in ['YES', 'NO']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.upper() == 'YES':
                self.consent_mgr.log_consent(user_id, 'all', True, "Full audit consent granted")
                await ctx.author.send("✅ Full audit consent granted!")
            else:
                self.consent_mgr.log_consent(user_id, 'all', False)
                await ctx.author.send("❌ Full audit consent denied")
        except:
            await ctx.author.send("⏱️ Consent request timed out")
    
    @commands.command(name='revoke_consent')
    async def revoke_consent(self, ctx):
        """Revoke all consents"""
        user_id = ctx.author.id
        self.consent_mgr.revoke_all_consent(user_id)
        await ctx.author.send("✅ All consents have been revoked!")

async def setup(bot):
    await bot.add_cog(ConsentCommands(bot))
