import discord
from discord.ext import commands
import aiohttp

WEBHOOK_URL = "https://discord.com/api/webhooks/1397393135369322588/mbVcm2qbqZJYHFc-N83Fdbw-dyj7rbR1Bgg8fQ3IYEezYrogIR8viVlEwVUUQbw-YW5w"

class Suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggestion", help="Send a suggestion to the creator of this bot!", aliases=["suggest"])
    async def suggestion(self, ctx, *, suggestion_text: str = None):
        if not suggestion_text:
            await ctx.send("❌ Please provide a suggestion after the command.")
            return

        embed = discord.Embed(
            title="New Suggestion",
            description=suggestion_text,
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {ctx.author.id}")

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)
            await webhook.send(embed=embed)

        await ctx.send("✅ Your suggestion has been sent. Thank you!")

async def setup(bot):
    await bot.add_cog(Suggestion(bot))
