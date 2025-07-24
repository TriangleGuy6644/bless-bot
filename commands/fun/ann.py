import discord
from discord.ext import commands
import random

class Ann(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Add your GIF URLs here (Discord CDN or reliable direct links)
        self.gifs = [
            "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTV4NGNpMHFyOWR0eDR0cTB1djM3YndoeGR4bmY0Z2FveTBzbGd1YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qpNqbkL5z0OWaRdhul/giphy.gif"
            "https://tenor.com/btDFq.gif",
            "https://tenor.com/v60IoMhS1Tu.gif",
            "https://tenor.com/lAflNx93Wag.gif"
        ]

    @commands.command()
    async def template(self, ctx, user: discord.Member = None):
        if user is None:
            return await ctx.send("You need to mention someone! Example: `!template @user`")

        if not self.gifs:
            return await ctx.send("No GIFs have been added yet!")

        chosen_gif = random.choice(self.gifs)

        embed = discord.Embed(
            description=f"{ctx.author.mention} did something to {user.mention}!",
            color=discord.Color.blue()
        )
        embed.set_image(url=chosen_gif)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ann(bot))
