import discord
from discord.ext import commands

class HeavenCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.heaven_gif = "https://media.discordapp.net/attachments/1396954735826960495/1397025910540075059/heaven.gif?ex=68803944&is=687ee7c4&hm=8a529b7de1fb004a4ea829ddd3d24db691f4719e09e03307548a203cca27fefc&="

    @commands.command(name="heaven", help="Sends a message to heaven", aliases=["ascend"])
    async def heaven(self, ctx):
        if not ctx.message.reference:
            await ctx.send("You must reply to a message to send it to heaven ☁️")
            return

        try:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except Exception:
            await ctx.send("Couldn’t find the original message 😿")
            return

        embed = discord.Embed(
            title="A message has ascended :face_holding_back_tears:",
            description=f"\"{replied_message.content}\"\n— {replied_message.author.mention}",
            color=discord.Color.gold()
        )
        embed.set_image(url=self.heaven_gif)
        embed.set_footer(text=f"Sent by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HeavenCommand(bot))
