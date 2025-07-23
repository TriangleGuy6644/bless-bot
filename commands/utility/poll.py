import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, ctx, *, question: str):
        embed = discord.Embed(
            title="📊 New Poll!",
            description=question,
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Poll started by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

async def setup(bot):
    await bot.add_cog(Poll(bot))
