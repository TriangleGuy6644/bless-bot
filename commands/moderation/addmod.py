import discord
from discord.ext import commands
import json
import os

MOD_ROLES_FILE = "mod_roles.json"

def load_mod_roles():
    if not os.path.exists(MOD_ROLES_FILE):
        with open(MOD_ROLES_FILE, "w") as f:
            json.dump({}, f)
    with open(MOD_ROLES_FILE, "r") as f:
        return json.load(f)

def save_mod_roles(data):
    with open(MOD_ROLES_FILE, "w") as f:
        json.dump(data, f, indent=4)

class AddMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mod_roles = load_mod_roles()

    @commands.command(name="addmod", help="Assign a role permission to run moderation commands. Usage: !addmod @role")
    @commands.has_permissions(administrator=True)
    async def addmod(self, ctx, role: discord.Role):
        guild_id = str(ctx.guild.id)
        role_id = str(role.id)

        if guild_id not in self.mod_roles:
            self.mod_roles[guild_id] = []

        if role_id in self.mod_roles[guild_id]:
            await ctx.send(f"❌ The role {role.name} is already a mod role.")
            return

        self.mod_roles[guild_id].append(role_id)
        save_mod_roles(self.mod_roles)

        await ctx.send(f"✅ The role {role.mention} can now use moderation commands.")

    # Utility method for other cogs to check if a user has a mod role
    def is_mod(self, member: discord.Member):
        guild_id = str(member.guild.id)
        if guild_id not in self.mod_roles:
            return False

        mod_role_ids = self.mod_roles[guild_id]
        return any(str(role.id) in mod_role_ids for role in member.roles)

async def setup(bot):
    await bot.add_cog(AddMod(bot))
