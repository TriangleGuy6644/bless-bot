import discord
from discord.ext import commands
import json
import os
import time
import random

SHRIMP_DATA_FILE = "shrimp_data.json"
COOLDOWN_SECONDS = 5

RARITIES = [
    "Grade F", "Grade D", "Grade C", "Grade B",
    "Grade A", "Grade S", "Grade S+", "Ultimate"
]

SHRIMP_BY_RARITY = {
    "Grade F": [
        "Wild neocardina shrimp", "Blue rii shrimp", "Yellow sakura shrimp", "Black rii shrimp"
    ],
    "Grade D": [
        "Cherry shrimp", "Sakura neocardina shrimp", "Blue velvet shrimp", "Blue dream shrimp", "Yellow fire shrimp"
    ],
    "Grade C": [
        "Orange sakura shrimp", "Amano shrimp", "Highgrade sakura shrimp", "Green jade shrimp",
        "Red rii shrimp", "Blue rii shrimp", "Yellow rii shrimp"
    ],
    "Grade B": [
        "Wood shrimp", "Snowball shrimp", "Black rii shrimp", "Orange rii shrimp",
        "Fire-red neocardina shrimp", "Blue diamond shrimp", "Golden back yellow shrimp"
    ],
    "Grade A": [
        "Painted-fire-red neocardina shrimp", "Blue carbon rii shrimp"
    ],
    "Grade S": [
        "Bloody mary shrimp", "Blue carbon shrimp",
        "High-grade-yellow-fire neocardina shrimp", "Choclate neocardina shrimp"
    ],
    "Grade S+": [
        "Purple dream shrimp", "White rii shrimp", "Carbon rii shrimp", "Green jade shrimp", "Orange pumpkin shrimp"
    ],
    "Ultimate": [
        "Solid-purple-dream neocardina shrimp"
    ]
}

# Rarity weights (higher = more common)
RARITY_WEIGHTS = [50, 20, 10, 7, 5, 4, 2, 0.2]


def load_shrimp_data():
    if not os.path.exists(SHRIMP_DATA_FILE):
        with open(SHRIMP_DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(SHRIMP_DATA_FILE, "r") as f:
        return json.load(f)


def save_shrimp_data(data):
    with open(SHRIMP_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


class InventoryPaginator(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=60)
        self.pages = pages
        self.index = 0

    async def update_page(self, interaction):
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index > 0:
            self.index -= 1
            await self.update_page(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index < len(self.pages) - 1:
            self.index += 1
            await self.update_page(interaction)


class Shrimping(commands.GroupCog, group_name="sfish"):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_shrimp_data()

    async def cog_unload(self):
        save_shrimp_data(self.data)

    @commands.group(invoke_without_command=True)
    async def sfish(self, ctx):
        """Fish for a random shrimp!"""
        if ctx.invoked_subcommand is not None:
            return

        user_id = str(ctx.author.id)
        now = int(time.time())
        user = self.data.get(user_id, {"last_sfish": 0, "inventory": {}, "stats": {}})
        time_since_last = now - user.get("last_sfish", 0)
        if time_since_last < COOLDOWN_SECONDS:
            remaining = COOLDOWN_SECONDS - time_since_last
            await ctx.send(f"⏳ You must wait {remaining} seconds before shrimping again!")
            return

        rarity = random.choices(RARITIES, weights=RARITY_WEIGHTS, k=1)[0]
        shrimp = random.choice(SHRIMP_BY_RARITY[rarity])

        # Inventory and stats update
        inventory = user.setdefault("inventory", {})
        inventory[shrimp.lower()] = inventory.get(shrimp.lower(), 0) + 1

        stats = user.setdefault("stats", {})
        stats[rarity] = stats.get(rarity, 0) + 1

        user["last_sfish"] = now
        self.data[user_id] = user
        save_shrimp_data(self.data)

        await ctx.send(f"🦐 You caught a **{shrimp}**! ({rarity})")

    @sfish.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx):
        """Show your shrimp inventory (paginated)"""
        user_id = str(ctx.author.id)
        user = self.data.get(user_id, {"inventory": {}})
        inventory = user.get("inventory", {})
        if not inventory:
            await ctx.send("You have no shrimp yet!")
            return

        items = list(inventory.items())
        items_per_page = 10
        pages = []

        for i in range(0, len(items), items_per_page):
            embed = discord.Embed(
                title=f"{ctx.author.display_name}'s Shrimp Inventory",
                color=discord.Color.purple()
            )
            for name, count in items[i:i + items_per_page]:
                embed.add_field(name=name.title(), value=f"×{count}", inline=True)
            embed.set_footer(text=f"Page {len(pages) + 1}")
            pages.append(embed)

        view = InventoryPaginator(pages)
        await ctx.send(embed=pages[0], view=view)

    @sfish.command(name="give", aliases=["send", "g"])
    async def give(self, ctx, member: discord.Member, *, shrimp_name: str):
        """Give shrimp to another user"""
        user_id = str(ctx.author.id)
        target_id = str(member.id)
        user = self.data.get(user_id, {"inventory": {}})
        inventory = user.get("inventory", {})

        shrimp_name = shrimp_name.lower()
        amount = 1

        if inventory.get(shrimp_name, 0) < amount:
            await ctx.send(f"You don't have enough {shrimp_name.title()} to give!")
            return
        inventory[shrimp_name] -= amount
        if inventory[shrimp_name] == 0:
            del inventory[shrimp_name]

        target = self.data.get(target_id, {"inventory": {}, "stats": {}})
        target_inventory = target.setdefault("inventory", {})
        target_inventory[shrimp_name] = target_inventory.get(shrimp_name, 0) + amount

        self.data[user_id] = user
        self.data[target_id] = target
        save_shrimp_data(self.data)
        await ctx.send(f"Gave {amount} {shrimp_name.title()} to {member.mention}!")

    @sfish.command(name="stats", aliases=["stat", "s"])
    async def stats(self, ctx):
        """Show your shrimping stats"""
        user_id = str(ctx.author.id)
        user = self.data.get(user_id, {"stats": {}})
        stats = user.get("stats", {})
        if not stats:
            await ctx.send("No stats yet!")
            return

        total_casts = sum(stats.get(r, 0) for r in RARITIES)
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Shrimp Stats",
            color=discord.Color.teal()
        )
        embed.add_field(name="Total Casts", value=str(total_casts), inline=False)
        for rarity in RARITIES:
            count = stats.get(rarity, 0)
            embed.add_field(name=rarity, value=str(count), inline=True)
        await ctx.send(embed=embed)

    @sfish.command(name="list", aliases=["shrimplist"])
    async def list_shrimp(self, ctx):
        lines = []
        for rarity in RARITIES:
            shrimp_list = SHRIMP_BY_RARITY.get(rarity, [])
            if shrimp_list:
                shrimp_str = ", ".join(shrimp_list)
                lines.append(f"**{rarity}**: {shrimp_str}")
        msg = "\n".join(lines)
        await ctx.send(msg)

    @sfish.command(name="flex", aliases=["showoff", "brag"])
    async def flex(self, ctx, *, shrimp_name: str):
        user_id = str(ctx.author.id)
        user = self.data.get(user_id, {"inventory": {}})
        inventory = user.get("inventory", {})
        shrimp_name = shrimp_name.lower()
        count = inventory.get(shrimp_name, 0)
        if count == 0:
            await ctx.send(f"You don't have any {shrimp_name.title()} to flex!")
            return
        await ctx.send(f"{ctx.author.mention} is flexing their **{shrimp_name.title()}**! They have **{count}** of them!")


async def setup(bot):
    await bot.add_cog(Shrimping(bot))
