# commands/lockdown.py
import discord
from discord.ext import commands

class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lockdown", help="Lock or unlock the current channel.")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, mode: str):
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)

        if mode.lower() == "on":
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(embed=discord.Embed(
                title="🔒 Channel Locked",
                description=f"{channel.mention} is now in lockdown. Members can't send messages.",
                color=discord.Color.red()
            ))

        elif mode.lower() == "off":
            overwrite.send_messages = None  # Resets to default
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(embed=discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{channel.mention} is now unlocked. Members can send messages again.",
                color=discord.Color.green()
            ))

        else:
            await ctx.send("❌ Invalid mode! Use `!lockdown on` or `!lockdown off`.")

async def setup(bot):
    await bot.add_cog(Lockdown(bot))
