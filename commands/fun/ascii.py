import discord
from discord.ext import commands
import pyfiglet

class Ascii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ascii", help="Convert text to ASCII art")
    async def ascii(self, ctx, *, text: str):
        if len(text) > 30:
            await ctx.send("❌ Text too long. Please use 30 characters or fewer.")
            return

        result = pyfiglet.figlet_format(text)
        if len(result) > 1900:
            await ctx.send("❌ ASCII result too long to send.")
            return

        await ctx.send(f"```{result}```")

async def setup(bot):
    await bot.add_cog(Ascii(bot))
