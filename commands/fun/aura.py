import discord
from discord.ext import commands
import json
import os
import random
# 1369175793241952259
AURA_FILE = "aura_data.json"
SPECIAL_USER_IDS = {
    1369175793241952259, #me
    662280043426349057, # moco
    1372572863193681991, # gato
    965662029870428181, # oscar
    771006273671266384, #
}

def load_data():
    if not os.path.exists(AURA_FILE):
        with open(AURA_FILE, "w") as f:
            json.dump({}, f)
    with open(AURA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(AURA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Aura(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    def get_balance(self, user_id):
        if user_id in SPECIAL_USER_IDS:
            return float('inf')  # infinite Aura
        return self.data.get(str(user_id), 0)

    def set_balance(self, user_id, amount):
        if user_id in SPECIAL_USER_IDS:
            return  # Don't store infinite users' balances
        self.data[str(user_id)] = amount
        save_data(self.data)

    @commands.command(name="aura", help="Check your current Aura balance")
    async def aura(self, ctx):
        bal = self.get_balance(ctx.author.id)
        if bal == float('inf'):
            await ctx.send(f"{ctx.author.mention}, you have **infinite Aura**! ✨")
        else:
            await ctx.send(f"{ctx.author.mention}, you have **{bal} Aura**.")

    @commands.command(name="giveaura", help="Give Aura to another user. Usage: !giveaura @user auratop", aliases=["agive", "gaura"])
    async def giveaura(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("You must give a positive amount of Aura!")
            return

        giver_id = ctx.author.id
        receiver_id = member.id

        giver_balance = self.get_balance(giver_id)

        # Infinite aura users always have enough
        if giver_id not in SPECIAL_USER_IDS and giver_balance < amount:
            await ctx.send("You don't have enough Aura to give!")
            return

        # Subtract from giver unless infinite
        if giver_id not in SPECIAL_USER_IDS:
            self.set_balance(giver_id, giver_balance - amount)

        receiver_balance = self.get_balance(receiver_id)
        # Add to receiver unless infinite (optional)
        if receiver_id not in SPECIAL_USER_IDS:
            self.set_balance(receiver_id, receiver_balance + amount)

        await ctx.send(f"{ctx.author.mention} gave {amount} Aura to {member.mention}!")

    @commands.command(name="auratop", help="Show the Aura leaderboard", aliases=["atop"])
    async def auratop(self, ctx):
        if not self.data:
            await ctx.send("No Aura data yet!")
            return

        leaderboard = self.data.copy()
        # Add infinite users to leaderboard with infinite Aura
        for uid in SPECIAL_USER_IDS:
            leaderboard[str(uid)] = float('inf')

        # Sort descending by balance
        sorted_balances = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

        embed = discord.Embed(title="Aura Leaderboard", color=discord.Color.blue())
        for i, (user_id, bal) in enumerate(sorted_balances[:10], start=1):
            user = self.bot.get_user(int(user_id))
            name = user.name if user else f"User ID {user_id}"
            val = "∞ (Infinite Aura)" if bal == float('inf') else f"{bal} Aura"
            embed.add_field(name=f"{i}. {name}", value=val, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="aurafarm", help="Farm a random amount of Aura between 10 and 100")
    @commands.cooldown(1, 60, commands.BucketType.user)  # 60-second cooldown per user
    async def aurafarm(self, ctx):
        amount = random.randint(10, 100)
        user_id = ctx.author.id

        # Add the aura
        current_balance = self.get_balance(user_id)
        if user_id not in SPECIAL_USER_IDS:
            self.set_balance(user_id, current_balance + amount)

        await ctx.send(f"🌟 {ctx.author.mention}, you farmed **{amount} Aura**! You now have **{'∞' if current_balance == float('inf') else current_balance + amount} Aura**.")

    @aurafarm.error
    async def aurafarm_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Slow down! You can farm Aura again in {int(error.retry_after)} seconds.")

    @commands.command(name="aurareset", help="Reset all users' Aura except special users. Owner only.")
    async def aurareset(self, ctx):
        if ctx.author.id != 1369175793241952259:
            await ctx.send("❌ You don't have permission to use this command.")
            return

        # Clear all aura except for special user IDs
        new_data = {}
        for user_id in self.data:
            if int(user_id) in SPECIAL_USER_IDS:
                new_data[user_id] = self.data[user_id]

        self.data = new_data
        save_data(self.data)

        await ctx.send("✅ All Aura balances have been reset except special users.")

async def setup(bot):
    await bot.add_cog(Aura(bot))
