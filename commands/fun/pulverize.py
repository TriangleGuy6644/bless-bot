import discord
from discord.ext import commands
import random

class Pulverize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1397376855824273478/8f7b25ee13cfd669418c78cd50431de3.gif?ex=6881801c&is=68802e9c&hm=170a59f1cb1ddac7b9c50e3aea84fdf4f774b2f0b813b6d2f2c4530312229e27&=",
            "https://media.discordapp.net/attachments/1396954735826960495/1397376856587632772/cecda1422cb7aa6252b970ef28a14b63.gif?ex=6881801c&is=68802e9c&hm=b66648a7e46ea8b544686e77919ce5e1741d308bccb877446f82da2c0c06d685&="
            # Add more pulverizing GIFs here
        ]

    @commands.command(name="pulverize", help="Pulverizes the tagged user.", aliases=["atomize"])
    async def pulverize(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("❌ You need to mention someone to pulverize.")
            return

        gif = random.choice(self.gifs)

        embed = discord.Embed(
            title="💥 Pulverized",
            description=f"{ctx.author.mention} pulverized {member.mention} into dust!",
            color=discord.Color.orange()
        )
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Pulverize(bot))
