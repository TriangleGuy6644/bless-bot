import discord
from discord.ext import commands
import random

class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Add your GIF URLs here (Discord CDN or reliable direct links)
        self.gifs = [
            # "https://link-to-gif1.gif",
            # "https://link-to-gif2.gif",
            # Add more GIF URLs here
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
    await bot.add_cog(Template(bot))
