import discord
from discord.ext import commands
from PIL import Image, ImageOps
import aiohttp
import io

class ExeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def exe(self, ctx, user: discord.Member = None):
        """Fetches a user's avatar and sends an inverted version of it."""
        if user is None:
            await ctx.send("You need to mention someone. Example: `!exe @user`")
            return

        avatar_url = user.display_avatar.replace(format="png", size=256).url

        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                if resp.status != 200:
                    await ctx.send("Couldn't fetch the avatar.")
                    return

                data = await resp.read()

        with Image.open(io.BytesIO(data)) as im:
            im = im.convert("RGBA")  # Ensure image is in RGBA
            r, g, b, a = im.split()
            rgb_image = Image.merge("RGB", (r, g, b))
            inverted_image = ImageOps.invert(rgb_image)
            final_image = Image.merge("RGBA", (*inverted_image.split(), a))

            output_buffer = io.BytesIO()
            final_image.save(output_buffer, format="PNG")
            output_buffer.seek(0)

        file = discord.File(output_buffer, filename="inverted.png")
        await ctx.send(f"🔄 Inverted avatar of {user.mention}", file=file)

async def setup(bot):
    await bot.add_cog(ExeCommand(bot))
