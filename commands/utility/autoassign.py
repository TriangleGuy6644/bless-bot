import discord
from discord.ext import commands
import json
import os

AUTOASSIGN_FILE = "autoassign_roles.json"

def load_autoassign():
    if not os.path.exists(AUTOASSIGN_FILE):
        with open(AUTOASSIGN_FILE, "w") as f:
            json.dump({}, f)
    with open(AUTOASSIGN_FILE, "r") as f:
        return json.load(f)

def save_autoassign(data):
    with open(AUTOASSIGN_FILE, "w") as f:
        json.dump(data, f, indent=4)

class AutoAssign(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_autoassign()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def autoassign(self, ctx, role: discord.Role = None):
        """Autoassigns a role to all members and future joiners."""
        if role is None:
            await ctx.send("You need to mention a role. Example: `!autoassign @role`")
            return

        self.data[str(ctx.guild.id)] = role.id
        save_autoassign(self.data)

        # Assign role to all current members
        assigned = 0
        failed = 0
        await ctx.send(f"Assigning `{role.name}` to all members...")

        for member in ctx.guild.members:
            if role in member.roles or member.bot:
                continue
            try:
                await member.add_roles(role, reason="Autoassign role")
                assigned += 1
            except:
                failed += 1

        await ctx.send(f"✅ Done! Assigned to {assigned} members. Failed: {failed}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        role_id = self.data.get(guild_id)
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role, reason="Autoassign on join")
                except:
                    pass

async def setup(bot):
    await bot.add_cog(AutoAssign(bot))
