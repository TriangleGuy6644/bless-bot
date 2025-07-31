import discord
from discord.ext import commands
import json
import os

OAO_DATA_FILE = "oao_data.json"
OWNER_ID = 1369175793241952259  # User allowed to set the one and only

def load_oao_data():
    if not os.path.exists(OAO_DATA_FILE):
        with open(OAO_DATA_FILE, "w") as f:
            json.dump({"one_and_only": None}, f)
    with open(OAO_DATA_FILE, "r") as f:
        return json.load(f)

def save_oao_data(data):
    with open(OAO_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class OneAndOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_oao_data()

    @commands.command()
    async def oao(self, ctx):
        """Show the one and only king."""
        user_id = self.data.get("one_and_only")
        if user_id is None:
            await ctx.send("No one and only user has been set yet.")
            return

        user = ctx.guild.get_member(user_id)
        if user is None:
            await ctx.send("The one and only user is not in this server.")
            return

        embed = discord.Embed(
            title="The One and Only King is...",
            description=f"{user.mention} 👑",
            color=discord.Color.gold()
        )   
        await ctx.send(embed=embed)

    @commands.command()
    async def oaoadd(self, ctx, member: discord.Member = None):
        """Set the one and only user. Only usable by OWNER_ID."""
        if ctx.author.id != OWNER_ID:
            await ctx.send("You are not authorized to use this command.")
            return
        if member is None:
            await ctx.send("You must mention a user to set as the one and only.")
            return
        self.data["one_and_only"] = member.id
        save_oao_data(self.data)
        await ctx.send(f"{member.mention} has been set as the one and only user.")

async def setup(bot):
    await bot.add_cog(OneAndOnly(bot))
