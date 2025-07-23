import discord
from discord.ext import commands

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="whois")
    async def whois(self, ctx, member: discord.Member = None):
        member = member or ctx.author  # Default to command runner

        embed = discord.Embed(
            title=f"Who is {member.display_name}?",
            color=discord.Color.green()
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Username", value=str(member), inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)

        # Exact account creation time
        embed.add_field(
            name=":information: Joined Discord",
            value=f"<t:{int(member.created_at.timestamp())}:F>",
            inline=False
        )

        # Exact server join time
        embed.add_field(
            name="📥 Joined This Server",
            value=f"<t:{int(member.joined_at.timestamp())}:F>" if member.joined_at else "Unknown",
            inline=False
        )

        # Roles (except @everyone)
        roles = [role.mention for role in member.roles[1:]]  # skip @everyone
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "None", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Whois(bot))
