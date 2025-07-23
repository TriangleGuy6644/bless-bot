import discord
from discord.ext import commands

class MemberCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mc")
    async def mc(self, ctx):
        guild = ctx.guild
        count = guild.member_count

        embed = discord.Embed(
            title="📊 Member Count",
            description=f"This server has **{count}** members!",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberCount(bot))
