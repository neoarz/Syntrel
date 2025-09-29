import discord
from discord.ext import commands
from discord.ext.commands import Context

from .translate import translate_command

class Utilities(commands.GroupCog, name="utilities"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="utilities", invoke_without_command=True)
    async def utilities_group(self, context: Context):
        embed = discord.Embed(
            title="Utilities Commands",
            description="Use `.utilities <subcommand>` or `/utilities <subcommand>`.",
            color=0x7289DA
        )
        embed.add_field(name="Available", value="translate", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, **kwargs):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command, **kwargs)
        else:
            await context.send(f"Unknown utilities command: {name}")

    @utilities_group.command(name="translate")
    async def utilities_group_translate(self, context: Context, text: str = None, to_lang: str = "en", from_lang: str = None):
        await self._invoke_hybrid(context, "translate", text=text, to_lang=to_lang, from_lang=from_lang)

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
