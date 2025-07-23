import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands", "h"])
    async def help(self, ctx):
        embed = discord.Embed(
            title="📜 Command Help Menu",
            description="Here's a categorized list of all available commands.",
            color=discord.Color.purple()
        )

        embed.set_footer(text="Made by @spaderequiem", icon_url=self.bot.user.display_avatar.url)

        # General
        embed.add_field(
            name="🛠️ General",
            value="`!ping`, `!avatar`, `!whois`, `!ascii`, `!coinflip`, `!8ball`, `!funfact`, `!goats`, `!hof`, `!quote`",
            inline=False
        )

        #Moderation
        embed.add_field(
            name="⚔ Moderation",
            value="`!kick`, `!ban`, `!timeout`, `!mute`, `!warn`, `!purge`, `!delwarn`, `!warns`, `!lockdown`, "
        )


        # Social & Fun
        embed.add_field(
            name="🎭 Fun & Social",
            value="`!crack`, `!beer`, `!fban`, `!raid`, `!liedetector`, `!heaven`, `!incinerate`, `!explode`, `!patrick`, `!assassinate`, `!execute`, `!pulverize`",
            inline=False
        )

        # Currency
        embed.add_field(
            name="Aura",
            value="`!aura`, `!giveaura`, `!auratop`, `!aurafarm`",
            inline=False
        )


        # Info APIs
        embed.add_field(
            name="🌐 Info APIs",
            value="`!weather`, `!steam`, `!mcskin`, `!quote`, `!urban`, `!dic`, `!wiki`",
            inline=False
        )


        # reddit
        embed.add_field(
            name="📱 Reddit",
            value="`!reddit`, `!redditpost / !rt`, `!redditnsfw`, `!cute`, `!cat`, `!femboy`",
            inline=False
        )

        # Fishing
        embed.add_field(
            name="🎣 Fishing",
            value="`!fish`, `!fish stats`, `!fish inventory`, `!fish flex`, `!fish give`, `!fish list`",
            inline=False
        )


        #meta
        embed.add_field(
            name="Suggestions",
            value="Suggest new features to Bless with the `!suggest` command!",
            inline=False
        )

        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
