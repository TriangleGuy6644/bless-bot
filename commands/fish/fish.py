import discord
from discord.ext import commands
import json
import os
import time
import random

FISH_DATA_FILE = "fish_data.json"
COOLDOWN_SECONDS = 5

RARITIES = [
    "common", "uncommon", "rare", "epic", "ultra rare", "legendary", "mythic", "heavenly", "???", "10000 Cast Special"
]

FISH_BY_RARITY = {
    "common": [
        "Cod", "Salmon", "Trout", "Herring", "Sardine", "Flying Fish", "Minnow", "Bream",
        "Common Carp", "Lilypad", "Duckweed", "Tire", "Metal Bar", "Smallmouth Bass",
        "Sea Bass", "Largemouth Bass", "Sunfish"
    ],
    "uncommon": [
        "Perch", "Carp", "Catfish", "Roach", "Tilapia", "Redtail Catfish", "Oyster", "Rasbora",
        "Dragonfly Larvae", "Mirror Carp", "Frog", "Newt", "Turtle", "Snapping Turtle"
    ],
    "rare": [
        "Pike", "Zander", "Bass", "Snapper", "Mackerel", "Flounder",
        "Hybrid Carp", "Starfish", "Chilli Rasbora", "Emerald Rasbora", "Neon Tetra", "Guppy"
    ],
    "epic": [
        "Eel", "Tuna", "Swordfish", "Sturgeon", "Barramundi",
        "Ghost Carp", "Scandinavian Perch"
    ],
    "ultra rare": [
        "Marlin", "Dorado", "Tarpon", "Grouper", "Halibut",
        "Amano Shrimp", "Cherry Shrimp", "Kooli Loach"
    ],
    "legendary": [
        "Musky", "Golden Carp", "Leviathan", "Kraken", "Ancient Salmon", "Moco Fish",
        "Gigantic Catfish", "Albino Pike"
    ],
    "mythic": [
        "Poseidon’s Wrasse", "Phoenix Fish", "Dragonfish", "Seraphim Eel", "Celestial Koi",
        "Goldfish", "Oarfish"
    ],
    "heavenly": [
        "Angel Fish", "Divine Tuna", "Holy Pike", "Paradise Carp", "Blessed Bass",
        "Asian Stone Catfish", "Jellyfish"
    ],
    "???": [
        "Cthulhu", "Cosmic Cod", "Void Salmon", "Eldritch Eel", "Infinity Perch",
        "Electric Eel", "Lionfish", "King Jellyfish", "Black Seal", "Electric Jellyfish",
        "Box Jellyfish", "Cookiecutter Shark"
    ],
    "10000 Cast Special": ["Albino Musky"]
}

def load_fish_data():
    if not os.path.exists(FISH_DATA_FILE):
        with open(FISH_DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(FISH_DATA_FILE, "r") as f:
        return json.load(f)

def save_fish_data(data):
    with open(FISH_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class PaginatorView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=60)
        self.pages = pages
        self.current = 0

    async def update(self, interaction):
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current > 0:
            self.current -= 1
            await self.update(interaction)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current < len(self.pages) - 1:
            self.current += 1
            await self.update(interaction)

class Fishing(commands.GroupCog, group_name="fish"):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_fish_data()

    async def cog_unload(self):
        save_fish_data(self.data)

    @commands.group(invoke_without_command=True)
    async def fish(self, ctx):
        user_id = str(ctx.author.id)
        now = int(time.time())
        user = self.data.get(user_id, {"last_fish": 0, "inventory": {}, "stats": {}})
        time_since_last = now - user.get("last_fish", 0)

        if time_since_last < COOLDOWN_SECONDS:
            remaining = COOLDOWN_SECONDS - time_since_last
            await ctx.send(f"⏳ Wait {remaining} more seconds.")
            return

        rarity = random.choices(list(FISH_BY_RARITY), weights=[50,20,10,7,5,4,2,1,0.5,0.1])[0]
        fish = random.choice(FISH_BY_RARITY[rarity])

        inventory = user.setdefault("inventory", {})
        inventory[fish] = inventory.get(fish, 0) + 1
        stats = user.setdefault("stats", {})
        stats[rarity] = stats.get(rarity, 0) + 1

        user["last_fish"] = now
        self.data[user_id] = user
        save_fish_data(self.data)

        await ctx.send(f"🎣 You caught a **{fish}**! ({rarity.title()})")

    @fish.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx):
        user_id = str(ctx.author.id)
        user = self.data.get(user_id, {"inventory": {}})
        inventory = user.get("inventory", {})

        if not inventory:
            await ctx.send("You have no fish!")
            return

        fish_items = list(inventory.items())
        per_page = 10
        pages = []

        for i in range(0, len(fish_items), per_page):
            embed = discord.Embed(
                title=f"{ctx.author.display_name}'s Fish Inventory",
                color=discord.Color.blurple()
            )
            for fish, count in fish_items[i:i+per_page]:
                embed.add_field(name=fish, value=f"×{count}", inline=True)
            embed.set_footer(text=f"Page {i//per_page + 1}/{(len(fish_items) - 1)//per_page + 1}")
            pages.append(embed)

        view = PaginatorView(pages)
        await ctx.send(embed=pages[0], view=view)

    @fish.command(name="give", aliases=["send", "g"])
    async def give(self, ctx, member: discord.Member, fish_name: str, amount: int = 1):
        user_id = str(ctx.author.id)
        target_id = str(member.id)
        user = self.data.get(user_id, {"inventory": {}})
        inventory = user.get("inventory", {})
        fish_name = fish_name.title()

        if inventory.get(fish_name, 0) < amount:
            await ctx.send("You don’t have enough of that fish.")
            return

        inventory[fish_name] -= amount
        if inventory[fish_name] == 0:
            del inventory[fish_name]

        target = self.data.get(target_id, {"inventory": {}, "stats": {}})
        target_inventory = target.setdefault("inventory", {})
        target_inventory[fish_name] = target_inventory.get(fish_name, 0) + amount

        self.data[user_id] = user
        self.data[target_id] = target
        save_fish_data(self.data)

        await ctx.send(f"Gave {amount} {fish_name} to {member.mention}.")

    @fish.command(name="stats")
    async def stats(self, ctx):
        user_id = str(ctx.author.id)
        user = self.data.get(user_id, {"stats": {}})
        stats = user.get("stats", {})

        if not stats:
            await ctx.send("No stats yet.")
            return

        total = sum(stats.get(r, 0) for r in RARITIES)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Stats", color=discord.Color.green())
        embed.add_field(name="Total Casts", value=str(total), inline=False)

        for rarity in RARITIES:
            count = stats.get(rarity, 0)
            if count > 0:
                embed.add_field(name=rarity.title(), value=str(count), inline=True)

        await ctx.send(embed=embed)

    @fish.command(name="list")
    async def list_fish(self, ctx):
        lines = []
        for rarity in RARITIES:
            fish_list = FISH_BY_RARITY.get(rarity, [])
            if fish_list:
                lines.append(f"{rarity.title()}: {', '.join(fish_list)}")
        await ctx.send("\n".join(lines))

    @fish.command(name="flex")
    async def flex(self, ctx, *, fish_name: str):
        user_id = str(ctx.author.id)
        user = self.data.get(user_id, {"inventory": {}})
        inventory = user.get("inventory", {})
        fish_name = fish_name.title()
        count = inventory.get(fish_name, 0)
        if count == 0:
            await ctx.send(f"You don't own any {fish_name}.")
            return
        await ctx.send(f"{ctx.author.mention} is flexing their **{fish_name}** x{count}!")

async def setup(bot):
    await bot.add_cog(Fishing(bot))
