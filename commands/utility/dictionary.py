import discord
from discord.ext import commands
import aiohttp

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dic", aliases=["define", "dictionary"], help="Get a definition of an English word")
    async def dic(self, ctx, *, word: str):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("❌ Couldn't fetch the definition.")
                    return

                data = await response.json()

        if isinstance(data, dict) and data.get("title") == "No Definitions Found":
            await ctx.send(f"❌ No definition found for '{word}'.")
            return

        entry = data[0]
        meanings = entry.get("meanings", [])
        if not meanings:
            await ctx.send(f"❌ No meanings available for '{word}'.")
            return

        definition = meanings[0]["definitions"][0]["definition"]
        part_of_speech = meanings[0].get("partOfSpeech", "unknown")
        example = meanings[0]["definitions"][0].get("example", "No example available.")

        embed = discord.Embed(
            title=f"Definition of {word}",
            description=f"**{part_of_speech.capitalize()}**\n{definition}",
            color=discord.Color.green()
        )
        if example:
            embed.add_field(name="Example", value=example, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Dictionary(bot))
