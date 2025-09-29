import discord
from discord.ext import commands
from discord.ext.commands import Context

from .idevice import idevice_command
from .error_codes import errorcodes_command
from .developermode import developermode_command
from .noapps import noapps_command
from .mountddi import mountddi_command

class Idevice(commands.GroupCog, name="idevice"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(
        name="idevice",
        description="Get help with idevice commands and troubleshooting."
    )
    async def idevice(self, context):
        return await idevice_command()(self, context)

    @commands.hybrid_command(
        name="errorcodes",
        description="Look up error codes and their meanings."
    )
    async def errorcodes(self, context, *, error_code: str = None):
        return await errorcodes_command()(self, context, error_code=error_code)

    @commands.hybrid_command(
        name="developermode",
        description="How to turn on developer mode"
    )
    async def developermode(self, context):
        return await developermode_command()(self, context)

    @commands.hybrid_command(
        name="noapps",
        description="Help when apps aren't showing in installed apps view"
    )
    async def noapps(self, context):
        return await noapps_command()(self, context)

    @commands.hybrid_command(
        name="mountddi",
        description="How to manually mount DDI"
    )
    async def mountddi(self, context):
        return await mountddi_command()(self, context)

async def setup(bot) -> None:
    cog = Idevice(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'idevice.idevice'")
    bot.logger.info("Loaded extension 'idevice.errorcodes'")
    bot.logger.info("Loaded extension 'idevice.developermode'")
    bot.logger.info("Loaded extension 'idevice.noapps'")
    bot.logger.info("Loaded extension 'idevice.mountddi'")
