import discord
from discord.ext import commands
import aiohttp
import random

class UrbanDictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ud", aliases=["urban"], help="Get a random Urban Dictionary definition for a word")
    async def ud(self, ctx, *, term: str):
        url = f"https://api.urbandictionary.com/v0/define?term={term}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("❌ Couldn't reach Urban Dictionary.")
                    return
                data = await response.json()

        if not data["list"]:
            await ctx.send(f"❌ No definitions found for `{term}`.")
            return

        entry = random.choice(data["list"])
        definition = entry["definition"][:1024]  # Discord embed field limit
        example = entry["example"][:1024] if entry["example"] else "No example provided."

        embed = discord.Embed(
            title=f"Urban Dictionary: {term}",
            description=definition,
            color=discord.Color.orange()
        )
        embed.add_field(name="Example", value=example, inline=False)
        embed.set_footer(text=f"👍 {entry['thumbs_up']} | 👎 {entry['thumbs_down']}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UrbanDictionary(bot))
