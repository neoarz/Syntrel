import discord
from discord.ext import commands
from discord.ext.commands import Context

from .translate import translate_command

class Utilities(commands.GroupCog, name="utilities"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(
        name="translate",
        description="Translate text to another language"
    )
    async def translate(self, context, text: str = None, to_lang: str = "en", from_lang: str = None):
        return await translate_command()(self, context, text=text, to_lang=to_lang, from_lang=from_lang)

async def setup(bot) -> None:
    cog = Utilities(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'utilities.translate'")
