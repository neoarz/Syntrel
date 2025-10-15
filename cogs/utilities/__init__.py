import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .translate import translate_command, language_autocomplete
from .codepreview import codepreview_command
from .dictionary import dictionary_command


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Utilities(commands.GroupCog, name="utils"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="utilities", aliases=["utils"], invoke_without_command=True)
    async def utilities_group(self, context: Context):
        embed = discord.Embed(
            title="Utilities Commands",
            description="Use `.utils <subcommand>` or `/utils <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="Utilities", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        embed.add_field(name="Available", value="translate, codepreview, dictionary", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, **kwargs):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command, **kwargs)
        else:
            await context.send(f"Unknown utilities command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @utilities_group.command(name="translate")
    @app_commands.describe(
        text="The text to translate",
        to_lang="Target language (e.g., 'en', 'es', 'fr')",
        from_lang="Source language (leave empty for auto-detect)"
    )
    @app_commands.autocomplete(to_lang=language_autocomplete)
    @app_commands.autocomplete(from_lang=language_autocomplete)
    async def utilities_group_translate(self, context: Context, text: str = None, to_lang: str = "en", from_lang: str = None):
        await self._invoke_hybrid(context, "translate", text=text, to_lang=to_lang, from_lang=from_lang)

    @utilities_group.command(name="codepreview")
    async def utilities_group_codepreview(self, context: Context, url: str = None):
        await self._invoke_hybrid(context, "codepreview", url=url)

    @utilities_group.command(name="dictionary")
    @app_commands.describe(
        word="The word to look up"
    )
    async def utilities_group_dictionary(self, context: Context, word: str = None):
        await self._invoke_hybrid(context, "dictionary", word=word)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="translate",
        description="Translate text to another language"
    )
    @app_commands.describe(
        text="The text to translate",
        to_lang="Target language (e.g., 'en', 'es', 'fr')",
        from_lang="Source language (leave empty for auto-detect)"
    )
    @app_commands.autocomplete(to_lang=language_autocomplete)
    @app_commands.autocomplete(from_lang=language_autocomplete)
    async def translate(self, context, text: str = None, to_lang: str = "en", from_lang: str = None):
        return await translate_command()(self, context, text=text, to_lang=to_lang, from_lang=from_lang)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="codepreview",
        description="Preview code from GitHub URLs"
    )
    async def codepreview(self, context, url: str = None):
        return await codepreview_command()(self, context, url=url)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="dictionary",
        description="Get the definition of a word"
    )
    @app_commands.describe(
        word="The word to look up"
    )
    async def dictionary(self, context, word: str = None):
        return await dictionary_command()(self, context, word=word)

async def setup(bot) -> None:
    cog = Utilities(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'utilities.translate'")
    bot.logger.info("Loaded extension 'utilities.codepreview'")
    bot.logger.info("Loaded extension 'utilities.dictionary'")
