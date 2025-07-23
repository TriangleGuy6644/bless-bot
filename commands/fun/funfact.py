import discord
from discord.ext import commands
import random
import os

CURRENT_DIR = os.path.dirname(__file__)
FACTS_FILE = os.path.join(CURRENT_DIR, "Facts.txt")

class FunFact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.facts = self.load_facts()

    def load_facts(self):
        if not os.path.exists(FACTS_FILE):
            return ["Fun fact file not found."]
        with open(FACTS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    @commands.command(name="funfact", aliases=["fact"])
    async def funfact(self, ctx):
        fact = random.choice(self.facts)
        embed = discord.Embed(title="Fun Fact", description=fact, color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunFact(bot))
