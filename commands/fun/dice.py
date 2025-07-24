import discord
from discord.ext import commands
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dice")
    async def dice(self, ctx, sides: int = 6):
        """Roll a dice with the given number of sides (default 6)."""
        if sides < 4 or sides > 100:
            await ctx.send("❌ Number of sides must be between 4 and 100.")
            return
        result = random.randint(1, sides)
        await ctx.send(f"🎲 You rolled a **{result}** on a **{sides}-sided** dice.")

async def setup(bot):
    await bot.add_cog(Dice(bot))
