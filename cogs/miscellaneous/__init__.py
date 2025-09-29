import discord
from discord.ext import commands
from discord.ext.commands import Context

from .rickroll import rr_command
from .labubu import labubu_command
from .tryitandsee import tryitandsee_command
from .piracy import piracy_command
from .keanu import keanu_command

class Miscellaneous(commands.GroupCog, name="miscellaneous"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(
        name="rr",
        description="Rickroll"
    )
    async def rr(self, context):
        return await rr_command()(self, context)

    @commands.hybrid_command(
        name="labubu",
        description="Labubu ASCII art"
    )
    async def labubu(self, context):
        return await labubu_command()(self, context)

    @commands.hybrid_command(
        name="tryitandsee",
        description="Try it and see"
    )
    async def tryitandsee(self, context):
        return await tryitandsee_command()(self, context)

    @commands.hybrid_command(
        name="piracy",
        description="FBI Anti Piracy Warning"
    )
    async def piracy(self, context):
        return await piracy_command()(self, context)

    @commands.hybrid_command(
        name="keanu",
        description="Reeves"
    )
    async def keanu(self, context):
        return await keanu_command()(self, context)

async def setup(bot) -> None:
    cog = Miscellaneous(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'miscellaneous.rr'")
    bot.logger.info("Loaded extension 'miscellaneous.labubu'")
    bot.logger.info("Loaded extension 'miscellaneous.tryitandsee'")
    bot.logger.info("Loaded extension 'miscellaneous.piracy'")
    bot.logger.info("Loaded extension 'miscellaneous.keanu'")
