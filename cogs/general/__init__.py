import discord
from discord.ext import commands
from discord.ext.commands import Context

from .ping import ping_command
from .uptime import uptime_command
from .botinfo import botinfo_command
from .serverinfo import serverinfo_command
from .feedback import feedback_command


def _require_group_prefix(context: Context) -> bool:
    if getattr(context, "interaction", None):
        return True
    group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
    if not group:
        return True
    prefix = context.prefix or ""
    content = context.message.content.strip().lower()
    return content.startswith(f"{prefix}{group} ")

class General(commands.GroupCog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="general", invoke_without_command=True)
    async def general_group(self, context: Context):
        embed = discord.Embed(
            title="General Commands",
            description="Use `.general <subcommand>` or `/general <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="General", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        embed.add_field(name="Available", value="ping, uptime, botinfo, serverinfo, feedback", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown general command: {name}")

    @general_group.command(name="ping")
    async def general_group_ping(self, context: Context):
        await self._invoke_hybrid(context, "ping")

    @general_group.command(name="uptime")
    async def general_group_uptime(self, context: Context):
        await self._invoke_hybrid(context, "uptime")

    @general_group.command(name="botinfo")
    async def general_group_botinfo(self, context: Context):
        await self._invoke_hybrid(context, "botinfo")

    @general_group.command(name="serverinfo")
    async def general_group_serverinfo(self, context: Context):
        await self._invoke_hybrid(context, "serverinfo")

    @general_group.command(name="feedback")
    async def general_group_feedback(self, context: Context):
        await self._invoke_hybrid(context, "feedback")

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context):
        return await ping_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="uptime",
        description="Check how long the bot has been running.",
    )
    async def uptime(self, context):
        return await uptime_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context):
        return await botinfo_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context):
        return await serverinfo_command()(self, context)

    @commands.check(_require_group_prefix)
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
