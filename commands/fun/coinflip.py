import discord
from discord.ext import commands
import random

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coin Flip", description=f"The coin landed on **{result}**!", color=discord.Color.gold())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
