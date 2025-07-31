import discord
from discord.ext import commands
import json
import os

GOAT_FILE = "goats.json"
GOAT_EMOJI = "🐐"
OWNER_ID = 1369175793241952259  # your Discord user ID

def load_goats():
    if not os.path.exists(GOAT_FILE):
        with open(GOAT_FILE, "w") as f:
            json.dump([], f)
    with open(GOAT_FILE, "r") as f:
        return json.load(f)

def save_goats(goat_list):
    with open(GOAT_FILE, "w") as f:
        json.dump(goat_list, f, indent=4)

class Goats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.goat_list = load_goats()

    @commands.command(name="goats")
    async def list_goats(self, ctx):
        if not self.goat_list:
            await ctx.send("No goats have been added yet.")
            return

        embed = discord.Embed(title="The Goats 🥹", color=discord.Color.gold())
        for uid in self.goat_list:
            user = self.bot.get_user(int(uid))
            name = user.mention if user else f"User ID {uid}"
            embed.add_field(name=GOAT_EMOJI, value=name, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="goatadd", aliases=["addgoat"])
    async def add_goat(self, ctx, member: discord.Member):
        if ctx.author.id != OWNER_ID:
            await ctx.send("Only the goatmaster may add new goats.")
            return

        if len(self.goat_list) >= 6:
            await ctx.send(f"The goat list is full! Only 5 people can be goats at a time. Remove someone before adding a new one.")
            return

        user_id = str(member.id)
        if user_id in self.goat_list:
            await ctx.send(f"{member.mention} is already a GOAT {GOAT_EMOJI}")
            return

        self.goat_list.append(user_id)
        save_goats(self.goat_list)
        await ctx.send(f"{member.mention} has been added to the GOAT list {GOAT_EMOJI}")

    @commands.command(name="removegoat", aliases=["goatremove", "ungoat"])
    async def remove_goat(self, ctx, member: discord.Member):
        if ctx.author.id != OWNER_ID:
            await ctx.send("Only the goatmaster may remove goats.")
            return

        user_id = str(member.id)
        if user_id not in self.goat_list:
            await ctx.send(f"{member.mention} is not in the GOAT list.")
            return

        self.goat_list.remove(user_id)
        save_goats(self.goat_list)
        await ctx.send(f"{member.mention} has been removed from the GOAT list.")

async def setup(bot):
    await bot.add_cog(Goats(bot))
