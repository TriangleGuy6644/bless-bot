import discord
from discord.ext import commands

class Credits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def credits(self, ctx):
        embed = discord.Embed(
            title="🎖️ Credits",
            description="A big thanks to everyone involved!",
            color=discord.Color.gold()
        )
        embed.add_field(name="Main Developer", value="<@1369175793241952259>", inline=False)
        embed.add_field(name="Secondary Developer", value="j1nx", inline=False)
        embed.add_field(name="Profile Picture Artist", value="<@914234788779556925>", inline=False)
        embed.set_footer(text="Thank you for using the bot!")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Credits(bot))
