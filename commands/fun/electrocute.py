import discord
from discord.ext import commands
import secrets  # use secrets instead of random

class Electrocute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1397388941224574997/killua-lightning-palm-2thswbd1vlm4t1cs.gif?ex=68818b5d&is=688039dd&hm=264563e6e76cff80cff00c2ee8e3b5f14898411d4ca448bd3846935b0fa99c44&=",
            "https://media.discordapp.net/attachments/1396954735826960495/1397388941748998144/e49a9b1aa7e5565f9ae2d0e090c606f0.gif?ex=68818b5d&is=688039dd&hm=1f8d255c717d8b0224482c0f77f59ea8f3f0b848d13b3d2ace68aa2b09c9ad16&="
            # Add more electric shock GIFs here
        ]

    @commands.command(name="electrocute", help="Electrocutes the tagged user.")
    async def electrocute(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("⚡ You need to mention someone to electrocute.")
            return

        gif = secrets.choice(self.gifs)

        embed = discord.Embed(
            title="⚡ Zapped!",
            description=f"{ctx.author.mention} electrocuted {member.mention}!",
            color=discord.Color.yellow()
        )
        embed.set_image(url=gif)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Electrocute(bot))
