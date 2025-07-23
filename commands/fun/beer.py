import discord
from discord.ext import commands

class BeerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="beer")
    async def beer(self, ctx, user: discord.Member = None):
        if user is None:
            return await ctx.send("You need to mention someone! Example: `!beer @username`")

        embed = discord.Embed(
            description=f"{ctx.author.mention} gave {user.mention} a beer! 🍺",
            color=discord.Color.gold()
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1396954735826960495/1396992631224930507/giphy.gif?ex=68801a46&is=687ec8c6&hm=4f7a9e21ac6364173a1e8177c939fcb4fc10886e0ae2bb7b76cf6948865d1e6e&=")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BeerCommand(bot))
