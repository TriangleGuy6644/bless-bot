import discord
from discord.ext import commands
import random

class IncinerateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # List of GIF URLs — add more here as you want
        self.gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1397016377205985380/genos-robot-idol-genos-renatoxd.gif?ex=68803063&is=687edee3&hm=973c084f0699d4f7520015fc447213cdcccd1b9a426a4fd1b26d6697f2778989&=",
            "https://media.discordapp.net/attachments/1396954735826960495/1397373478801506455/170441.gif?ex=68817cf7&is=68802b77&hm=653e5fd8a7126641fc8be826cdba96abe4685ceb50d3768f677e0bf8ddfee23e&="
            # Add more gif URLs as strings here
        ]

    @commands.command(name="incinerate", help="Exterminates the mentioned user with style!")
    async def incinerate(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please mention a user to incinerate! Syntax: `!incinerate @user`")
            return

        gif_url = random.choice(self.gifs)

        embed = discord.Embed(
            description=f"Incinerating {member.mention}...",
            color=discord.Color.red()
        )
        embed.set_author(name=f"{ctx.author.display_name} activated incineration!")
        embed.set_image(url=gif_url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(IncinerateCommand(bot))
