import discord
from discord.ext import commands
import lyricsgenius
import os

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        token = os.getenv("GENIUS_TOKEN")
        print(f"Genius token loaded: {bool(token)}")  # Confirm token presence
        self.genius = lyricsgenius.Genius(token, timeout=15, retries=3)
        self.genius.skip_non_songs = True
        self.genius.excluded_terms = ["(Remix)", "(Live)"]
        self.genius.remove_section_headers = True

    @commands.command(name="lyrics")
    async def lyrics(self, ctx, *, query: str):
        print(f"Command triggered! Query: {query}")
        await ctx.trigger_typing()
        try:
            song = self.genius.search_song(query)
            print(f"Song found: {song}")
            if not song:
                print("No lyric found for query.")
                await ctx.send("Lyrics not found.")
                return

            lyrics = song.lyrics
            if not lyrics:
                print("Lyrics data is empty.")
                await ctx.send("Lyrics data is empty.")
                return
            
            print(f"Lyrics length: {len(lyrics)}")

            if len(lyrics) > 1900:
                lyrics = lyrics[:1900] + "\n...[truncated]"

            embed = discord.Embed(
                title=f"{song.title} — {song.artist}",
                description=lyrics,
                color=discord.Color.blurple()
            )
            try:
                await ctx.send(embed=embed)
            except Exception as send_error:
                print(f"Error sending embed: {send_error}")
                await ctx.send("Failed to send lyrics embed.")

        except Exception as e:
            print(f"Exception in lyrics command: {type(e).__name__}: {e}")
            await ctx.send(f"An error occurred: {type(e).__name__}: {e}")

async def setup(bot):
    await bot.add_cog(Lyrics(bot))
