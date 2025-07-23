# commands/ban.py
import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", help="Ban a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided."):
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=discord.Embed(
                title="🔨 User Banned",
                description=f"{member.mention} was banned.\n**Reason:** {reason}",
                color=discord.Color.red()
            ))
        except Exception as e:
            await ctx.send(f"❌ Failed to ban: {e}")

async def setup(bot):
    await bot.add_cog(Ban(bot))
