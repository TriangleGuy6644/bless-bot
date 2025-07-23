import discord
from discord.ext import commands
import json
import os

HOF_FILE = "halloffame.json"
OWNER_ID = 1369175793241952259

def load_hof():
    if not os.path.exists(HOF_FILE):
        with open(HOF_FILE, "w") as f:
            json.dump({}, f)
    with open(HOF_FILE, "r") as f:
        return json.load(f)

def save_hof(data):
    with open(HOF_FILE, "w") as f:
        json.dump(data, f, indent=4)

class HallOfFame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hof = load_hof()

    @commands.command(name="halloffame", aliases=["hof"], help="Shows the Hall of Fame messages")
    async def halloffame(self, ctx):
        if not self.hof:
            await ctx.send("Hall of Fame is empty!")
            return

        embed = discord.Embed(title="🏆 Hall of Fame", color=discord.Color.gold())
        for i, (msg_id, data) in enumerate(self.hof.items(), start=1):
            author = data.get("author_name", "Unknown")
            content = data.get("content", "")
            jump_url = data.get("jump_url", "")
            display_content = (content[:100] + "...") if len(content) > 100 else content
            embed.add_field(
                name=f"{i}. By {author}",
                value=f"{display_content}\n[Jump to message]({jump_url})",
                inline=False
            )
            if i >= 10:
                break

        await ctx.send(embed=embed)

    @commands.command(name="hofadd", help="Add the replied-to message to the Hall of Fame. Owner only.", aliases=["addhof", "ahof", "hofa"])
    async def hofadd(self, ctx):
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ You are not authorized to use this command.")
            return

        if not ctx.message.reference:
            await ctx.send("❌ You must reply to a message to add it to the Hall of Fame.")
            return

        try:
            channel = ctx.channel
            ref_message = await channel.fetch_message(ctx.message.reference.message_id)
        except Exception:
            await ctx.send("❌ Couldn't fetch the replied message.")
            return

        msg_id = str(ref_message.id)
        if msg_id in self.hof:
            await ctx.send("This message is already in the Hall of Fame.")
            return

        self.hof[msg_id] = {
            "author_name": str(ref_message.author),
            "content": ref_message.content,
            "jump_url": ref_message.jump_url
        }
        save_hof(self.hof)

        await ctx.send(f"✅ Added message by {ref_message.author.mention} to the Hall of Fame!")

    @commands.command(name="hofremove", help="Remove a message from the Hall of Fame. Owner only.", aliases=["removehof", "rhf"])
    async def hofremove(self, ctx, msg_id: str = None):
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ You are not authorized to use this command.")
            return
        
        # If no message ID argument, try to get from replied message
        if not msg_id:
            if not ctx.message.reference:
                await ctx.send("❌ You must reply to a Hall of Fame message or provide its message ID.")
                return
            msg_id = str(ctx.message.reference.message_id)

        if msg_id not in self.hof:
            await ctx.send("❌ That message is not in the Hall of Fame.")
            return

        removed = self.hof.pop(msg_id)
        save_hof(self.hof)
        await ctx.send(f"✅ Removed message by {removed.get('author_name', 'Unknown')} from the Hall of Fame.")

async def setup(bot):
    await bot.add_cog(HallOfFame(bot))
