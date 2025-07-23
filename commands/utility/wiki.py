import discord
from discord.ext import commands
import aiohttp
import urllib.parse

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wiki", aliases=["wikipedia"], help="Search a topic on Wikipedia")
    async def wiki(self, ctx, *, query: str):
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as resp:
                if resp.status != 200:
                    await ctx.send("❌ Couldn't find that topic on Wikipedia.")
                    return
                data = await resp.json()

        if 'extract' not in data:
            await ctx.send("❌ Couldn't find a summary for that topic.")
            return

        embed = discord.Embed(
            title=data.get('title', 'Wikipedia Result'),
            description=data.get('extract', 'No summary found.'),
            url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
            color=discord.Color.dark_blue()
        )

        if 'thumbnail' in data and 'source' in data['thumbnail']:
            embed.set_thumbnail(url=data['thumbnail']['source'])

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Wiki(bot))
