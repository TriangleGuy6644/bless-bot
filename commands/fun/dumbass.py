import discord
from discord.ext import commands
import secrets  # Use this instead of random

class Mock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mock_gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1397371335021166682/patrick-s-patrick.gif",
            "https://media.discordapp.net/attachments/1396954735826960495/1397372161194459239/broom-sweep.gif",
            "https://media.discordapp.net/attachments/1396954735826960495/1397372059264356434/bh187-spongebob.gif",
        ]

    @commands.command(name="patrick", help="Mocks the replied message.", aliases=["dumbass"])
    async def mock(self, ctx):
        if not ctx.message.reference:
            await ctx.send("❌ You need to reply to a message to mock it.")
            return

        try:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            quoted = replied_message.content.strip()
            author = replied_message.author.display_name

            gif_url = secrets.choice(self.mock_gifs)

            embed = discord.Embed(
                description=f"*\"{quoted}\"*\n- ***{author}***",
                color=discord.Color.orange()
            )
            embed.set_image(url=gif_url)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Couldn't mock that message: {e}")

async def setup(bot):
    await bot.add_cog(Mock(bot))
