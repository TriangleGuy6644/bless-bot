import discord
from discord.ext import commands
import json
import os

WARNINGS_FILE = "warnings.json"

def load_warnings():
    if not os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "w") as f:
            json.dump({}, f)
    with open(WARNINGS_FILE, "r") as f:
        return json.load(f)

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = load_warnings()

    def save_warnings(self):
        with open(WARNINGS_FILE, "w") as f:
            json.dump(self.warnings, f, indent=4)

    @commands.command(name="warnings", help="Show all warnings of a user.")
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user_warnings = self.warnings.get(guild_id, {}).get(user_id, [])

        if not user_warnings:
            await ctx.send(f"{member.mention} has no warnings.")
            return

        embed = discord.Embed(
            title=f"⚠️ Warnings for {member}",
            color=discord.Color.orange()
        )

        for i, warning in enumerate(user_warnings, 1):
            embed.add_field(name=f"Warning {i}", value=warning, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Warnings(bot))
