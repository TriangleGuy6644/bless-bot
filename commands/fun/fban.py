import discord
from discord.ext import commands

class FakeBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fban")
    async def fake_ban(self, ctx, member: discord.Member = None, *, reason: str = "No reason provided."):
        if not member:
            return await ctx.send("Usage: `!fban @user [optional reason]`")

        embed = discord.Embed(
            title="User Banned",
            color=discord.Color.red()
        )
        embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Moderator", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Action logged • {discord.utils.format_dt(ctx.message.created_at, style='f')}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FakeBan(bot))
