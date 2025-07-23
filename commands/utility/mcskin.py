import discord
from discord.ext import commands
import aiohttp

class MinecraftSkin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mcskin(self, ctx, username: str):
        """Shows Minecraft user's NameMC profile and skin preview"""
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status != 200:
                    await ctx.send("❌ Username not found.")
                    return
                data = await r.json()

        uuid = data.get("id")
        name = data.get("name")

        namemc_link = f"https://namemc.com/profile/{uuid}"
        namemc_skin_preview = f"https://visage.surgeplay.com/full/512/{uuid}.png"

        embed = discord.Embed(
            title=f"Minecraft Skin for {name}",
            description=f"[View NameMC Profile]({namemc_link})",
            color=discord.Color.dark_green()
        )
        embed.set_image(url=namemc_skin_preview)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MinecraftSkin(bot))
