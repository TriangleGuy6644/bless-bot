import discord
from discord.ext import commands
import aiohttp
import random

class RedditDynamic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reddit", help="Fetch a random image from any subreddit", aliases=["redditimage", "ri"])
    async def reddit(self, ctx, subreddit: str):
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
        headers = {"User-Agent": "DiscordBot (by u/yourbotname)"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    await ctx.send(f"Couldn't fetch from r/{subreddit} 😞")
                    return
                data = await resp.json()

        posts = data["data"]["children"]
        image_posts = [
            p["data"] for p in posts
            if p["data"]["url"].endswith((".jpg", ".jpeg", ".png", ".gif"))
            and not p["data"].get("over_18", False)
        ]

        if not image_posts:
            await ctx.send(f"No safe posts found from r/{subreddit} 😢")
            return

        post = random.choice(image_posts)
        post_url = f"https://reddit.com{post['permalink']}"

        embed = discord.Embed(
            title=post["title"],
            url=post_url,
            description=f"From r/{subreddit}",
            color=discord.Color.random()
        )
        embed.set_image(url=post["url"])
        embed.set_footer(text=f"👍 {post['ups']} | 💬 {post['num_comments']}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RedditDynamic(bot))
