import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .baitbot import baitbot_command, BaitBotListener, has_protected_role
from .mention import MentionListener
from .stickybot import (
    stickybot_command,
    StickyBotListener,
    has_allowed_role as has_sticky_role,
)


def _require_group_prefix(context: Context) -> bool:
    if getattr(context, "interaction", None):
        return True
    group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
    if not group:
        return True
    prefix = context.prefix or ""
    content = context.message.content.strip().lower()
    return content.startswith(f"{prefix}{group} ")


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Events(commands.GroupCog, name="events"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="events", invoke_without_command=True)
    async def events_group(self, context: Context):
        embed = discord.Embed(
            title="Events Commands",
            description="Use `.events <subcommand>` or `/events <subcommand>`.",
            color=0x7289DA,
        )
        embed.set_author(
            name="Events", icon_url="https://yes.nighty.works/raw/eW5lLm.webp"
        )
        embed.add_field(name="Available", value="baitbot, stickybot", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, **kwargs):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command, **kwargs)
        else:
            await context.send(f"Unknown events command: {name}")

    @events_group.command(name="baitbot")
    @has_protected_role()
    async def events_group_baitbot(self, context: Context):
        await self._invoke_hybrid(context, "baitbot")

    @events_group.command(name="stickybot")
    @has_sticky_role()
    async def events_group_stickybot(self, context: Context):
        await self._invoke_hybrid(context, "stickybot")

    @commands.check(_require_group_prefix)
    @has_protected_role()
    @commands.hybrid_command(
        name="baitbot", description="View bait bot configuration and status."
    )
    async def baitbot(self, context):
        return await baitbot_command()(self, context)

    @commands.check(_require_group_prefix)
    @has_sticky_role()
    @commands.hybrid_command(
        name="stickybot", description="View sticky bot configuration and status."
    )
    async def stickybot(self, context):
        return await stickybot_command()(self, context)


async def setup(bot) -> None:
    cog = Events(bot)
    await bot.add_cog(cog)

    listener = BaitBotListener(bot)
    await bot.add_cog(listener)

    mention_listener = MentionListener(bot)
    await bot.add_cog(mention_listener)

    sticky_bot = StickyBotListener(bot)
    await bot.add_cog(sticky_bot)

    bot.logger.info("Loaded extension 'events.baitbot'")
    bot.logger.info("Loaded extension 'events.mention'")
    bot.logger.info("Loaded extension 'events.stickybot'")
