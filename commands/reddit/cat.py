import discord
from discord.ext import commands
import aiohttp
import random

class CatCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subreddits = ["cats", "catpictures", "catmemes"]

    @commands.command(name="cat", help="Sends a random cat image from Reddit")
    async def cat(self, ctx):
        subreddit = random.choice(self.subreddits)
        reddit_url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"

        headers = {"User-Agent": "DiscordBot (by u/yourbotname)"}

        async with aiohttp.ClientSession() as session:
            async with session.get(reddit_url, headers=headers) as resp:
                if resp.status != 200:
                    await ctx.send("Couldn't fetch a cat right now 🐾")
                    return
                data = await resp.json()

        posts = data["data"]["children"]
        image_posts = [p["data"] for p in posts if p["data"]["url"].endswith((".jpg", ".png", ".gif"))]

        if not image_posts:
            await ctx.send("No cats found 😿")
            return

        post = random.choice(image_posts)
        image_url = post["url"]
        title = post["title"]

        embed = discord.Embed(
            title=title,
            description=f"From r/{subreddit}",
            color=discord.Color.orange()
        )
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CatCommand(bot))
