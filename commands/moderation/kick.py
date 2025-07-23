# commands/kick.py
import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", help="Kick a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided."):
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=discord.Embed(
                title="👢 User Kicked",
                description=f"{member.mention} was kicked.\n**Reason:** {reason}",
                color=discord.Color.orange()
            ))
        except Exception as e:
            await ctx.send(f"❌ Failed to kick: {e}")

async def setup(bot):
    await bot.add_cog(Kick(bot))
