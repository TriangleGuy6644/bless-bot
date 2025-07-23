import discord
from discord.ext import commands
import aiohttp
import datetime

STEAM_API_KEY = "835A13F35F8A265CA618332BB6143C15"

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def resolve_vanity(self, session, vanity):
        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl={vanity}"
        async with session.get(url) as r:
            data = await r.json()
            if data["response"]["success"] != 1:
                return None
            return data["response"]["steamid"]

    async def get_player_summaries(self, session, steamid):
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid}"
        async with session.get(url) as r:
            data = await r.json()
            players = data.get("response", {}).get("players", [])
            if not players:
                return None
            return players[0]

    def is_steamid64(self, input_str):
        # SteamID64 is a 17-digit number starting usually with 7656...
        return input_str.isdigit() and len(input_str) == 17 and input_str.startswith("765")

    @commands.command()
    async def steam(self, ctx, user_input: str):
        """Get Steam profile info by vanity username or SteamID64"""
        async with aiohttp.ClientSession() as session:
            steamid = None

            if self.is_steamid64(user_input):
                steamid = user_input
            else:
                steamid = await self.resolve_vanity(session, user_input)

            if not steamid:
                await ctx.send("❌ Could not find that Steam user.")
                return

            player = await self.get_player_summaries(session, steamid)
            if not player:
                await ctx.send("❌ Could not fetch player info.")
                return

        created = datetime.datetime.utcfromtimestamp(player.get("timecreated", 0)).strftime("%Y-%m-%d %H:%M:%S UTC") if player.get("timecreated") else "N/A"

        status_map = {
            0: "Offline",
            1: "Online",
            2: "Busy",
            3: "Away",
            4: "Snooze",
            5: "Looking to trade",
            6: "Looking to play",
        }
        status = status_map.get(player.get("personastate", 0), "Unknown")

        embed = discord.Embed(
            title=player.get("personaname", "Unknown"),
            url=player.get("profileurl"),
            description=f"SteamID64: {steamid}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=player.get("avatarfull"))
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Account Created", value=created, inline=True)
        embed.add_field(name="Real Name", value=player.get("realname", "N/A"), inline=True)
        embed.add_field(name="Country", value=player.get("loccountrycode", "N/A"), inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Steam(bot))
