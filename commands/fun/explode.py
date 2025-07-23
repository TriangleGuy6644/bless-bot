import discord
from discord.ext import commands
import secrets

class Explode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gifs = [
            "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXNwN3RzdHp0b2g1bWl1cHNvZmI3M3lteHlwb3JldGtvY3A2c3J5ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SsxVZIX3NxZwMC2uhK/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzNzbnlobDh6ZDhsOWx0MWtnNnJmeXVhZ3dvc2N5ZmJpa2Z1cXllbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/eFifJQ2SUYxO0/giphy.gif"
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzNzbnlobDh6ZDhsOWx0MWtnNnJmeXVhZ3dvc2N5ZmJpa2Z1cXllbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3o7abwbzKeaRksvVaE/giphy.gif"
            # Add more explosion GIFs here
        ]

    @commands.command(name="explode", help="Explodes the tagged user.")
    async def explode(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("💥 You need to mention someone to explode.")
            return

        gif = secrets.choice(self.gifs)

        embed = discord.Embed(
            title="💥 Boom!",
            description=f"{ctx.author.mention} exploded {member.mention}!",
            color=discord.Color.red()
        )
        embed.set_image(url=gif)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Explode(bot))