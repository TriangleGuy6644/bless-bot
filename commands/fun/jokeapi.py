import discord
from discord.ext import commands
import aiohttp

class JokeAPICommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jokeapi", aliases=["joke"])
    async def jokeapi(self, ctx, category: str = "Any"):
        """Fetches a random joke from JokeAPI. Categories: Any, Programming, Dark, Pun, Spooky, Christmas"""

        url = f"https://v2.jokeapi.dev/joke/{category}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("❌ Failed to fetch a joke.")
                    return
                data = await resp.json()

        if data["error"]:
            await ctx.send("❌ JokeAPI returned an error.")
            return

        embed = discord.Embed(title=" Here's a joke for you, twin!", color=discord.Color.blurple())
        embed.set_footer(text=f"Category: {data.get('category', 'Unknown')}")

        if data["type"] == "single":
            embed.description = data["joke"]
        else:
            embed.description = f"**{data['setup']}**\n{data['delivery']}"

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(JokeAPICommand(bot))
