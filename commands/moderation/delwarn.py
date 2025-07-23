import discord
from discord.ext import commands
import json
import os

WARN_FILE = "warnings.json"

def load_warnings():
    if not os.path.exists(WARN_FILE):
        with open(WARN_FILE, "w") as f:
            json.dump({}, f)
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warnings(data):
    with open(WARN_FILE, "w") as f:
        json.dump(data, f, indent=4)

class DelWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = load_warnings()

    @commands.command(name="delwarn", help="Delete a warning by index or all warnings for a user. Usage: !delwarn @user [index/all]")
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, member: discord.Member, arg: str = None):
        user_id = str(member.id)
        if user_id not in self.warnings:
            await ctx.send(f"{member.mention} has no warnings.")
            return

        if arg is None:
            await ctx.send("Please specify the warning number to delete or `all` to remove all warnings.")
            return

        if arg.lower() == "all":
            self.warnings.pop(user_id)
            save_warnings(self.warnings)
            await ctx.send(f"All warnings for {member.mention} have been deleted.")
            return

        try:
            index = int(arg) - 1
            if index < 0 or index >= len(self.warnings[user_id]):
                await ctx.send(f"Invalid warning number. {member.mention} has {len(self.warnings[user_id])} warnings.")
                return

            removed = self.warnings[user_id].pop(index)
            if not self.warnings[user_id]:
                self.warnings.pop(user_id)  # Remove user if no warnings left

            save_warnings(self.warnings)
            await ctx.send(f"Deleted warning #{index+1} for {member.mention}: `{removed}`")

        except ValueError:
            await ctx.send("Invalid argument! Use a warning number or `all`.")

async def setup(bot):
    await bot.add_cog(DelWarn(bot))
