import discord
from discord.ext import commands
from discord.ext.commands import Context
import asyncio

# Make a pr to add your own server config here, you shouldn't need to touch the rest of the file, please fill in all the values for your own server
BAIT_CONFIGS = {
    "SideStore": {
        "guild_id": 949183273383395328,
        "channel_ids": [
            1432134748062482586,
            1432204211009097819,
        ],
        "protected_role_id": 959598279685963776,
        "log_channel_id": 1433532504647667823,
    },
    "neotest": {
        "guild_id": 1069946178659160076,
        "channel_ids": [
            1432175690270118012,
            1433987189670281278,
            1433988339031080991,
        ],
        "protected_role_id": 1432165329483857940,
        "log_channel_id": 1433987853184139365,
    },
    "idevice": {
        "guild_id": 1329314147434758175,
        "channel_ids": [
            1434317669695492177,
        ],
        "protected_role_id": 1333666918548111373,
        "log_channel_id": 1333673259446571022,
    },
    "melonx": {
        "guild_id": 1300369899704680479,
        "channel_ids": [
            1434327970679492830,
        ],
        "protected_role_id": 1300372178138697758,
        "log_channel_id": 1300374786471366696,
    },
}

BAN_REASON = "Detected bot/scammer in bait channel"


def has_protected_role():
    async def predicate(context: Context):
        if not context.guild:
            context.bot.logger.warning(
                f"[BAITBOT] Unauthorized baitbot command attempt by {context.author} ({context.author.id}) in DMs"
            )
            embed = discord.Embed(
                title="Permission Denied",
                description="You don't have permission to use this command.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png"
            )
            await context.send(embed=embed, ephemeral=True)
            return False

        if not hasattr(context.author, "roles"):
            context.bot.logger.warning(
                f"[BAITBOT] Unauthorized baitbot command attempt by {context.author} ({context.author.id}) in {context.guild.name} - no roles"
            )
            embed = discord.Embed(
                title="Permission Denied",
                description="You don't have permission to use this command.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png"
            )
            await context.send(embed=embed, ephemeral=True)
            return False

        for config in BAIT_CONFIGS.values():
            protected_role_id = config.get("protected_role_id")
            if protected_role_id:
                protected_role = context.guild.get_role(protected_role_id)
                if protected_role:
                    for role in context.author.roles:
                        if (
                            role.position >= protected_role.position
                            and role.id != context.guild.default_role.id
                        ):
                            return True

        context.bot.logger.warning(
            f"[BAITBOT] Unauthorized baitbot command attempt by {context.author} ({context.author.id}) in {context.guild.name} - insufficient role permissions"
        )
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xE02B2B,
        )
        embed.set_author(
            name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png"
        )
        await context.send(embed=embed, ephemeral=True)
        return False

    return commands.check(predicate)


def baitbot_command():
    async def wrapper(self, context: Context):
        embed = discord.Embed(
            title="Bait Bot",
            description="Bans people who post in a specific channel.",
            color=0x7289DA,
        )
        embed.set_author(
            name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png"
        )

        found_config = False
        if BAIT_CONFIGS:
            for name, config in BAIT_CONFIGS.items():
                guild_id = config.get("guild_id")
                if context.guild and guild_id == context.guild.id:
                    channel_ids = config.get("channel_ids", [])
                    if not channel_ids:
                        channel_id = config.get("channel_id")
                        if channel_id:
                            channel_ids = [channel_id]
                    role_id = config.get("protected_role_id", "Not set")

                    channel_displays = []
                    for channel_id in channel_ids:
                        channel = context.guild.get_channel(channel_id)
                        channel_display = (
                            f"<#{channel_id}> (`{channel_id}`)"
                            if channel
                            else f"`{channel_id}`"
                        )
                        channel_displays.append(channel_display)

                    channels_text = (
                        "\n".join(channel_displays) if channel_displays else "Not set"
                    )

                    role = context.guild.get_role(role_id)
                    role_display = (
                        f"<@&{role_id}> (`{role_id}`)" if role else f"`{role_id}`"
                    )

                    log_channel_id = config.get("log_channel_id")
                    log_channel = None
                    if log_channel_id:
                        log_channel = context.guild.get_channel(log_channel_id)
                    log_display = (
                        f"<#{log_channel_id}> (`{log_channel_id}`)"
                        if log_channel
                        else (f"`{log_channel_id}`" if log_channel_id else "Not set")
                    )

                    embed.add_field(
                        name="\u200b",
                        value=f"Channels:\n{channels_text}\n\nProtected Role:\n{role_display}\n\nLog Channel:\n{log_display}",
                        inline=False,
                    )
                    found_config = True

        if not found_config:
            embed.add_field(
                name="No Configurations",
                value="No bait channels configured for this server",
                inline=False,
            )

        if context.guild and context.guild.icon:
            embed.set_thumbnail(url=context.guild.icon.url)

        await context.send(embed=embed)

    return wrapper


class BaitBotListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return

        if message.author.bot:
            return

        bait_config = None
        config_name = None
        for name, config in BAIT_CONFIGS.items():
            if message.guild.id != config.get("guild_id"):
                continue

            channel_ids = config.get("channel_ids", [])
            if not channel_ids:
                channel_id = config.get("channel_id")
                if channel_id:
                    channel_ids = [channel_id]

            if message.channel.id in channel_ids:
                bait_config = config
                config_name = name
                break

        if not bait_config:
            return

        protected_role_id = bait_config.get("protected_role_id")
        is_protected = False
        if protected_role_id and hasattr(message.author, "roles"):
            protected_role = message.guild.get_role(protected_role_id)
            if protected_role:
                for role in message.author.roles:
                    if (
                        role.position >= protected_role.position
                        and role.id != message.guild.default_role.id
                    ):
                        self.bot.logger.info(
                            f"[BAITBOT] Skipped banning {message.author} ({message.author.id}) in #{message.channel.name}: protected role ({role.name})"
                        )
                        is_protected = True
                        break

        message_content = message.content if message.content else "*No text content*"
        message_attachments = message.attachments

        try:
            await message.delete()
            self.bot.logger.info(
                f"[BAITBOT] Deleted message from {message.author} in #{message.channel.name}"
            )
        except Exception as e:
            self.bot.logger.warning(
                f"[BAITBOT] Could not delete message from {message.author}: {e}"
            )
        banned = False
        if not is_protected:
            try:
                self.bot.logger.warning(
                    f"[BAITBOT] Detected user in bait channel [{config_name}]: {message.author.name} ({message.author.id}) in #{message.channel.name}"
                )

                if not message.guild.me.guild_permissions.ban_members:
                    self.bot.logger.error(
                        f"[BAITBOT] No permission to ban members in {message.guild.name}"
                    )
                else:
                    try:
                        await message.author.ban(
                            reason=BAN_REASON, delete_message_days=7
                        )
                        self.bot.logger.info(
                            f"[BAITBOT] Banned {message.author.name} - deleted messages from last 7 days"
                        )
                        banned = True
                    except discord.Forbidden:
                        self.bot.logger.error(
                            f"[BAITBOT] Could not ban {message.author.name}: missing permissions"
                        )
                    except Exception as e:
                        self.bot.logger.error(
                            f"[BAITBOT] Error banning {message.author.name}: {e}"
                        )

                    if banned:
                        await asyncio.sleep(2)
                        try:
                            await message.guild.unban(
                                message.author, reason="Auto-unban after cleanup"
                            )
                            self.bot.logger.info(
                                f"[BAITBOT] Unbanned {message.author.name} - cleanup complete"
                            )
                        except Exception as e:
                            self.bot.logger.error(
                                f"[BAITBOT] Error unbanning {message.author.name}: {e}"
                            )
            except Exception as e:
                self.bot.logger.error(f"[BAITBOT] Error handling bait message: {e}")

        log_channel_id = bait_config.get("log_channel_id")
        if log_channel_id:
            try:
                log_channel = self.bot.get_channel(log_channel_id)
                if log_channel:
                    action_text = (
                        "Message deleted (user banned and unbanned)"
                        if banned
                        else "Message deleted (protected user)"
                        if is_protected
                        else "Message deleted"
                    )
                    log_embed = discord.Embed(
                        title="Bait Bot",
                        description=action_text,
                        color=0xE02B2B,
                        timestamp=message.created_at,
                    )
                    log_embed.set_author(
                        name=str(message.author),
                        icon_url=message.author.display_avatar.url,
                    )
                    log_embed.add_field(
                        name="User", value=message.author.mention, inline=True
                    )
                    log_embed.add_field(
                        name="Channel", value=message.channel.mention, inline=True
                    )

                    combined_content = []
                    if message_content and message_content != "*No text content*":
                        combined_content.append(message_content)

                    image_url = None
                    if message_attachments:
                        for attachment in message_attachments:
                            if (
                                attachment.content_type
                                and attachment.content_type.startswith("image/")
                            ):
                                if not image_url:
                                    image_url = attachment.url
                            combined_content.append(attachment.filename)

                    content_text = (
                        "\n".join(combined_content)
                        if combined_content
                        else "*No content*"
                    )
                    if len(content_text) > 1000:
                        content_text = content_text[:997] + "..."

                    log_embed.add_field(
                        name="Content", value=f"```\n{content_text}\n```", inline=False
                    )

                    if image_url:
                        log_embed.set_image(url=image_url)

                    log_embed.set_footer(text=f"Message ID: {message.id}")

                    try:
                        await log_channel.send(embed=log_embed)
                        self.bot.logger.info(
                            f"[BAITBOT] Sent log to #{log_channel.name}"
                        )
                    except discord.Forbidden:
                        self.bot.logger.error(
                            f"[BAITBOT] No permission to send log to #{log_channel.name}"
                        )
                    except Exception as e:
                        self.bot.logger.error(f"[BAITBOT] Error sending log: {e}")
                else:
                    self.bot.logger.warning(
                        f"[BAITBOT] Log channel {log_channel_id} not found"
                    )
            except Exception as e:
                self.bot.logger.error(f"[BAITBOT] Error handling log channel: {e}")
