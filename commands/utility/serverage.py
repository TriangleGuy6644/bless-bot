import discord
from discord.ext import commands
from datetime import datetime, timezone

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverage")
    async def serverage(self, ctx):
        print("!serverage command triggered")
        try:
            guild = ctx.guild
            print(f"Guild object: {guild}")
            if guild is None:
                print("Guild is None - command not run in a server")
                await ctx.send("This command can only be used in a server.")
                return

            created_at = guild.created_at  # offset-aware datetime
            print(f"Created at: {created_at}")

            now = datetime.now(timezone.utc)  # offset-aware UTC datetime
            age = now - created_at

            years = age.days // 365
            months = (age.days % 365) // 30
            days = (age.days % 365) % 30

            print(f"Age calculated: {years}y {months}m {days}d")

            embed = discord.Embed(
                title=f"Server Age: {guild.name}",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Created On", value=created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=False)
            embed.add_field(name="Age", value=f"{years} years, {months} months, {days} days", inline=False)
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            embed.set_footer(text=f"Server ID: {guild.id}")

            await ctx.send(embed=embed)
            print("Embed sent")

        except Exception as e:
            print(f"Exception in serverage command: {e}")
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
