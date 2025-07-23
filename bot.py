import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv 

load_dotenv()


TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!𝗵𝗲𝗹𝗽"))
        print(f"✅ Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # If the bot is mentioned
    if bot.user in message.mentions:
        embed = discord.Embed(
            title="Hey, I'm here!",
            description="The command prefix is `!`.\nRun `!help` to see the help menu!",
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Coded by @spaderequiem!", icon_url=bot.user.avatar.url if bot.user.avatar else None)
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


# Recursively load .py files in commands/ and subfolders
async def load_cogs():
    for root, dirs, files in os.walk('./commands'):
        for file in files:
            if file.endswith('.py') and not file.startswith('_'):
                # Convert path to dot notation: commands/fun/crack.py → commands.fun.crack
                rel_path = os.path.relpath(os.path.join(root, file), './commands')
                module_path = rel_path.replace(os.sep, '.').replace('.py', '')
                full_import = f'commands.{module_path}'
                try:
                    await bot.load_extension(full_import)
                    print(f"✅ Loaded: {full_import}")
                except Exception as e:
                    print(f"❌ Failed to load {full_import}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
