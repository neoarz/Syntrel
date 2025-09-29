import discord
from discord.ext import commands
from discord.ext.commands import Context

from .ping import ping_command
from .uptime import uptime_command
from .botinfo import botinfo_command
from .serverinfo import serverinfo_command
from .feedback import feedback_command

class General(commands.GroupCog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context):
        return await ping_command()(self, context)

    @commands.hybrid_command(
        name="uptime",
        description="Check how long the bot has been running.",
    )
    async def uptime(self, context):
        return await uptime_command()(self, context)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context):
        return await botinfo_command()(self, context)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context):
        return await serverinfo_command()(self, context)

    @commands.hybrid_command(
        name="feedback",
        description="Submit a feedback for the owners of the bot"
    )
    async def feedback(self, context):
        return await feedback_command()(self, context)

async def setup(bot) -> None:
    cog = General(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'general.ping'")
    bot.logger.info("Loaded extension 'general.uptime'")
    bot.logger.info("Loaded extension 'general.botinfo'")
    bot.logger.info("Loaded extension 'general.serverinfo'")
    bot.logger.info("Loaded extension 'general.feedback'")
