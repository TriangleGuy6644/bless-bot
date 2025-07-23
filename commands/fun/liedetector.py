import discord
from discord.ext import commands
import random

class LieDetectorCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.truth_image = "https://media.discordapp.net/attachments/1396954735826960495/1397017554656170084/correct-buzzer.gif?ex=6880317c&is=687edffc&hm=d4fedcb97d1e780be878831f441f80b8a1129a133c28b937d84a4baab13ab834&="
        self.lie_image = "https://media.discordapp.net/attachments/1396954735826960495/1397017702979076117/lie-detector-lier.gif?ex=6880319f&is=687ee01f&hm=b1216c824781f4f7943f125ada2bc103477b83d469db4f75d412dc6c2a5910cf&="

    @commands.command(name="liedetector", help="Detects if the replied message is truth or lie", aliases=["lie", "detector", "truth"])
    async def liedetector(self, ctx):
        # Check if command is used as a reply
        ref = ctx.message.reference
        if ref is None:
            await ctx.send("Please use this command as a reply to someone's message.")
            return

        # Fetch the replied message
        replied_msg = await ctx.channel.fetch_message(ref.message_id)

        # Randomly pick truth or lie
        result = random.choice(["Truth", "Lie"])

        # Choose corresponding image and embed color
        if result == "Truth":
            color = discord.Color.green()
            image_url = self.truth_image
        else:
            color = discord.Color.red()
            image_url = self.lie_image

        embed = discord.Embed(
            title="🕵️ Lie Detector",
            description=f"The lie detector says: **{result}!**",
            color=color
        )
        embed.add_field(name="Message being tested:", value=replied_msg.content or "(no text content)", inline=False)
        embed.set_image(url=image_url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LieDetectorCommand(bot))
