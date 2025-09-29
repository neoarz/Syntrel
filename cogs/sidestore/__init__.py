import discord
from discord.ext import commands
from discord.ext.commands import Context

from .sidestore import sidestore_command
from .refresh import refresh_command
from .code import code_command
from .crash import crash_command
from .pairing import pairing_command
from .server import server_command
from .afc import afc_command
from .udid import udid_command
from .half import half_command
from .sparse import sparse_command

class Sidestore(commands.GroupCog, name="sidestore"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(
        name="sidestore",
        description="SideStore troubleshooting help"
    )
    async def sidestore(self, context):
        return await sidestore_command()(self, context)

    @commands.hybrid_command(
        name="refresh",
        description="Help with refreshing or installing apps"
    )
    async def refresh(self, context):
        return await refresh_command()(self, context)

    @commands.hybrid_command(
        name="code",
        description="No code received when signing in with Apple ID"
    )
    async def code(self, context):
        return await code_command()(self, context)

    @commands.hybrid_command(
        name="crash",
        description="Help with SideStore crashing issues"
    )
    async def crash(self, context):
        return await crash_command()(self, context)

    @commands.hybrid_command(
        name="pairing",
        description="Help with pairing file issues"
    )
    async def pairing(self, context):
        return await pairing_command()(self, context)

    @commands.hybrid_command(
        name="server",
        description="Help with anisette server issues"
    )
    async def server(self, context):
        return await server_command()(self, context)

    @commands.hybrid_command(
        name="afc",
        description="Help with AFC Connection Failure issues"
    )
    async def afc(self, context):
        return await afc_command()(self, context)

    @commands.hybrid_command(
        name="udid",
        description="SideStore could not determine device UDID"
    )
    async def udid(self, context):
        return await udid_command()(self, context)

    @commands.hybrid_command(
        name="half",
        description="Help with half-installed apps"
    )
    async def half(self, context):
        return await half_command()(self, context)

    @commands.hybrid_command(
        name="sparse",
        description="Help with sparse bundle issues"
    )
    async def sparse(self, context):
        return await sparse_command()(self, context)

async def setup(bot) -> None:
    cog = Sidestore(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'sidestore.sidestore'")
    bot.logger.info("Loaded extension 'sidestore.refresh'")
    bot.logger.info("Loaded extension 'sidestore.code'")
    bot.logger.info("Loaded extension 'sidestore.crash'")
    bot.logger.info("Loaded extension 'sidestore.pairing'")
    bot.logger.info("Loaded extension 'sidestore.server'")
    bot.logger.info("Loaded extension 'sidestore.afc'")
    bot.logger.info("Loaded extension 'sidestore.udid'")
    bot.logger.info("Loaded extension 'sidestore.half'")
    bot.logger.info("Loaded extension 'sidestore.sparse'")
