import discord
from discord.ext import commands
import secrets  # more secure random choice

class Execute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gifs = [
            "https://media.discordapp.net/attachments/1396954735826960495/1397375022313504858/PartisanExecutionWW2_USA.gif?ex=68817e67&is=68802ce7&hm=bd6f256fb708964021b095d5231bfe59175e8f6f060e2b66844deb4766329738&=",
            "https://media.discordapp.net/attachments/1396954735826960495/1397375021873365002/d76c34cadc4d8b83a145e10e31022d72.gif?ex=68817e67&is=68802ce7&hm=81f233d8fb9740f93557fa5f329b4d14b2476aa29051192725b27238be505bf7&="
            # Add more execution-style gifs here
        ]

    @commands.command(name="execute", help="Executes the tagged user.")
    async def execute(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("❌ You need to mention someone to execute.")
            return

        gif = secrets.choice(self.gifs)

        embed = discord.Embed(
            title="⚔️ Execution Order Carried Out",
            description=f"Executing {member.mention}...",
            color=discord.Color.dark_red()
        )
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Execute(bot))
