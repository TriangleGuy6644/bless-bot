import discord
from discord.ext import commands
import json
import random
import os

QUOTES_FILE = "quotes.json"

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        quotes_path = os.path.join(os.path.dirname(__file__), "..", "..", QUOTES_FILE)
        with open(quotes_path, "r", encoding="utf-8", errors="replace") as f:
            self.quotes = json.load(f)

    @commands.command(name="quote")
    async def quote(self, ctx):
        q = random.choice(self.quotes)
        quote_text = q.get("quoteText", "No quote found.")
        author = q.get("quoteAuthor", "Unknown")
        embed = discord.Embed(
            description=f"*{quote_text}*",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"— {author}" if author else "— Unknown")
        embed.set_author(name="Here's your quote!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Quote(bot))