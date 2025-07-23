import discord
from discord.ext import commands
import aiohttp
import random

class RedditText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="redditpost", aliases=["rt", "reddit-txt", "reddittext", "rpost"])
    async def reddit_text(self, ctx, subreddit: str):
        """Fetch a random text post from a subreddit."""
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=100&t=all"
        headers = {"User-Agent": "DiscordBot (by u/yourusername)"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    await ctx.send(f"Couldn't fetch posts from r/{subreddit}. Maybe it doesn't exist or is private.")
                    return
                data = await resp.json()

        posts = data.get("data", {}).get("children", [])
        text_posts = [
            post["data"] for post in posts
            if post["data"].get("selftext") and len(post["data"]["selftext"]) > 0
        ]

        if not text_posts:
            await ctx.send(f"No text posts found in r/{subreddit}!")
            return

        post = random.choice(text_posts)

        embed = discord.Embed(
            title=post["title"],
            url=f"https://reddit.com{post['permalink']}",
            color=discord.Color.orange()
        )
        # Limit description length to avoid huge messages
        description = post["selftext"]
        if len(description) > 1024:
            description = description[:1021] + "..."

        embed.description = description
        embed.set_footer(text=f"From r/{subreddit} | 👍 {post['ups']} | 💬 {post['num_comments']}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RedditText(bot))
