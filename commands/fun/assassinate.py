import discord
from discord.ext import commands
import random

class Assassinate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1397374149432705074/wZFl9v.gif",
            "https://media.discordapp.net/attachments/1396954735826960495/1397374150271569960/agent-47-hitman.gif",
            "https://media.discordapp.net/attachments/1396954735826960495/1397374150863093872/aGqL7Kb.gif"
            # Add more assassination gifs here
        ]

    @commands.command(name="assassinate", help="Assassinates the tagged user.")
    async def assassinate(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("❌ You need to mention someone to assassinate.")
            return

        gif = random.choice(self.gifs)

        embed = discord.Embed(
            title="🗡️ Target Eliminated",
            description=f"{ctx.author.mention} assassinated {member.mention}!",
            color=discord.Color.dark_red()
        )
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Assassinate(bot))
