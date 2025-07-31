import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.command(name="translate")
    async def translate(self, ctx):
        if ctx.message.reference is None:
            await ctx.send("Please reply to a message to translate it.")
            return

        try:
            replied_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except Exception:
            await ctx.send("Couldn't fetch the replied message.")
            return

        text = replied_msg.content
        if not text:
            await ctx.send("The replied message has no text to translate.")
            return

        try:
            detected = self.translator.detect(text)
            detected_lang = detected.lang
            print(f"Detected language: {detected_lang}")

            if detected_lang == 'en':
                await ctx.send("The message is already in English.")
                return

            translated = self.translator.translate(text, dest='en')
            translated_text = translated.text

            detected_lang_name = LANGUAGES.get(detected_lang, detected_lang).title()

            embed = discord.Embed(title="Translation", color=discord.Color.blurple())
            embed.add_field(name="Original Language", value=detected_lang_name, inline=False)
            embed.add_field(name="Original Text", value=text, inline=False)
            embed.add_field(name="Translated Text", value=translated_text, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred during translation: {e}")
            print(f"Translation error: {e}")

async def setup(bot):
    await bot.add_cog(Translate(bot))
