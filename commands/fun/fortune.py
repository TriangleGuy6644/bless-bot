import discord
from discord.ext import commands
import random
import os

class FortuneCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fortunes = self.load_all_fortunes("fortunes")

    def load_fortunes_from_file(self, filepath):
        if not os.path.isfile(filepath):
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip('\n') for line in f]

        fortunes = []
        current_fortune = []

        for line in lines:
            if line.strip() == '%':
                if current_fortune:
                    fortunes.append('\n'.join(current_fortune).strip())
                    current_fortune = []
            else:
                current_fortune.append(line)

        if current_fortune:
            fortunes.append('\n'.join(current_fortune).strip())

        return fortunes

    def load_all_fortunes(self, folder):
        all_fortunes = []
        if not os.path.isdir(folder):
            return ["(No fortune folder found!)"]

        for filename in os.listdir(folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(folder, filename)
                all_fortunes.extend(self.load_fortunes_from_file(filepath))

        if not all_fortunes:
            return ["(No fortunes found!)"]
        return all_fortunes

    @commands.command(name="fortune", help="Get a random fortune")
    async def fortune(self, ctx):
        fortune = random.choice(self.fortunes)
        embed = discord.Embed(
            title="🔮 Your Fortune",
            description=fortune,
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FortuneCommand(bot))
