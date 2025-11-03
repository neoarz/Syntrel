import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .ban import ban_command
from .kick import kick_command
from .purge import purge_command
from .warnings import warnings_command
from .archive import archive_command
from .hackban import hackban_command
from .nick import nick_command
from .timeout import timeout_command


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Moderation(commands.GroupCog, name="moderation"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="moderation", invoke_without_command=True)
    async def moderation_group(self, context: Context):
        embed = discord.Embed(
            title="Moderation Commands",
            description="Use `.moderation <subcommand>` or `/moderation <subcommand>`.",
            color=0x7289DA,
        )
        embed.add_field(
            name="Available",
            value="ban, kick, purge, warnings, archive, hackban, nick, timeout",
            inline=False,
        )
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, **kwargs):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command, **kwargs)
        else:
            await context.send(f"Unknown moderation command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    async def timeout_duration_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        options = [
            ("60 secs", "60s"),
            ("5 mins", "5m"),
            ("10 mins", "10m"),
            ("1 hour", "1h"),
            ("1 day", "1d"),
            ("1 week", "1w"),
        ]
        q = (current or "").lower()
        results: list[app_commands.Choice[str]] = []
        for name, value in options:
            if q in name.lower() or q in value.lower():
                results.append(app_commands.Choice(name=name, value=value))
        return results[:25]

    @moderation_group.command(name="ban")
    async def moderation_group_ban(
        self,
        context: Context,
        user: discord.User,
        *,
        reason: str = "Not specified",
        delete_messages: str = "none",
    ):
        await self._invoke_hybrid(
            context, "ban", user=user, reason=reason, delete_messages=delete_messages
        )

    @moderation_group.command(name="kick")
    async def moderation_group_kick(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ):
        await self._invoke_hybrid(context, "kick", user=user, reason=reason)

    @moderation_group.command(name="purge")
    async def moderation_group_purge(
        self, context: Context, amount: int, user: discord.Member = None
    ):
        await self._invoke_hybrid(context, "purge", amount=amount, user=user)

    @moderation_group.command(name="warnings")
    async def moderation_group_warnings(self, context: Context):
        await self._invoke_hybrid(context, "warnings")

    @moderation_group.command(name="archive")
    async def moderation_group_archive(self, context: Context, limit: int = 10):
        await self._invoke_hybrid(context, "archive", limit=limit)

    @moderation_group.command(name="hackban")
    async def moderation_group_hackban(
        self, context: Context, user_id: str, *, reason: str = "Not specified"
    ):
        await self._invoke_hybrid(context, "hackban", user_id=user_id, reason=reason)

    @moderation_group.command(name="nick")
    async def moderation_group_nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ):
        await self._invoke_hybrid(context, "nick", user=user, nickname=nickname)

    @moderation_group.command(name="timeout")
    async def moderation_group_timeout(
        self,
        context: Context,
        user: discord.User,
        duration: str,
        *,
        reason: str = "Not specified",
    ):
        await self._invoke_hybrid(
            context, "timeout", user=user, duration=duration, reason=reason
        )

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(name="ban", description="Bans a user from the server.")
    async def ban(
        self,
        context,
        user: discord.User,
        *,
        reason: str = "Not specified",
        delete_messages: str = "none",
    ):
        return await ban_command()(
            self, context, user=user, reason=reason, delete_messages=delete_messages
        )

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(name="kick", description="Kicks a user from the server.")
    async def kick(self, context, user: discord.User, *, reason: str = "Not specified"):
        return await kick_command()(self, context, user=user, reason=reason)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(name="purge", description="Delete a number of messages.")
    async def purge(self, context, amount: int, user: discord.Member = None):
        return await purge_command()(self, context, amount=amount, user=user)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="warnings", description="Manage warnings of a user on a server."
    )
    async def warnings(self, context):
        return await warnings_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="archive",
        description="Archives in a text file the last messages with a chosen limit of messages.",
    )
    async def archive(self, context, limit: int = 10):
        return await archive_command()(self, context, limit=limit)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
    )
    async def hackban(self, context, user_id: str, *, reason: str = "Not specified"):
        return await hackban_command()(self, context, user_id=user_id, reason=reason)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="nick", description="Change the nickname of a user on a server."
    )
    async def nick(self, context, user: discord.User, *, nickname: str = None):
        return await nick_command()(self, context, user=user, nickname=nickname)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="timeout", description="Timeout a user for a specified duration."
    )
    @app_commands.describe(
        user="The user that should be timed out.",
        duration="Duration",
        reason="The reason why the user should be timed out.",
    )
    @app_commands.autocomplete(duration=timeout_duration_autocomplete)
    async def timeout(
        self,
        context,
        user: discord.User,
        duration: str,
        *,
        reason: str = "Not specified",
    ):
        return await timeout_command()(
            self, context, user=user, duration=duration, reason=reason
        )


async def setup(bot) -> None:
    cog = Moderation(bot)
    await bot.add_cog(cog)

    bot.logger.info("Loaded extension 'moderation.ban'")
    bot.logger.info("Loaded extension 'moderation.kick'")
    bot.logger.info("Loaded extension 'moderation.purge'")
    bot.logger.info("Loaded extension 'moderation.warnings'")
    bot.logger.info("Loaded extension 'moderation.archive'")
    bot.logger.info("Loaded extension 'moderation.hackban'")
    bot.logger.info("Loaded extension 'moderation.nick'")
    bot.logger.info("Loaded extension 'moderation.timeout'")
