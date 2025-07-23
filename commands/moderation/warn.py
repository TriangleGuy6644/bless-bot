# commands/warn.py
import discord
from discord.ext import commands

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}  # In-memory warning storage. Replace with file/db if needed.

    @commands.command(name="warn", help="Warn a member. Syntax: !warn @member [reason]")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided."):
        if member == ctx.author:
            await ctx.send("❌ You can't warn yourself.")
            return
        if member == ctx.guild.owner:
            await ctx.send("❌ You can't warn the server owner.")
            return
        if member.bot:
            await ctx.send("❌ You can't warn a bot.")
            return

        # Save warning (temporary in-memory, can persist later)
        self.warns.setdefault(str(member.id), []).append(reason)

        embed = discord.Embed(
            title="⚠️ Member Warned",
            description=f"{member.mention} has been warned.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Warned by", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Warn(bot))
