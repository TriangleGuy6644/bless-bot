import discord
from discord.ext import commands
import aiohttp

API_KEY = "bd5e378503939ddaee76f12ad7a97608"

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, city: str):
        """Get current weather for a city"""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status != 200:
                    await ctx.send("❌ Could not find that city.")
                    return
                data = await r.json()

        name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        weather = data["weather"][0]["description"].title()
        icon = data["weather"][0]["icon"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        embed = discord.Embed(
            title=f"🌤️ Weather in {name}, {country}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}.png")
        embed.add_field(name="Condition", value=weather, inline=True)
        embed.add_field(name="Temperature", value=f"{temp}°C (feels like {feels}°C)", inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="Wind Speed", value=f"{wind} m/s", inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
