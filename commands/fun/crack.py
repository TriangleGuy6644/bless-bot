import discord
from discord.ext import commands
import random

class CrackCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # List your GIF URLs here (Discord CDN or reliable direct links)
        self.gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1396959531543826610/tenor.gif?ex=687ffb72&is=687ea9f2&hm=7b6780deb3c0cf8a6df82101d5c7d2033095edcf55427802843b1dbcb31d6f39&=",
            "https://media.discordapp.net/attachments/1396954735826960495/1396961256593948703/backshots-working-out.gif?ex=687ffd0d&is=687eab8d&hm=d7d1fcbfdb0181701ceaa5e46bc6cd25d584de5262f74db0e771a5e0ffb605f3&=",
            "https://media.discordapp.net/attachments/1396954735826960495/1396962171849801788/gojo-satoru.gif?ex=687ffde8&is=687eac68&hm=208bf09b74540aa15366e8522711b8e121feccc54ecada17e22f64d5335895fb&="
            # add more GIF URLs here
        ]

    @commands.command()
    async def crack(self, ctx, user: discord.Member = None):
        if user is None:
            return await ctx.send("You need to mention someone! Example: `!crack @user`")

        chosen_gif = random.choice(self.gifs)

        embed = discord.Embed(
            description=f"{ctx.author.mention} cracked {user.mention}! 💥",
            color=discord.Color.red()
        )
        embed.set_image(url=chosen_gif)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CrackCommand(bot))
