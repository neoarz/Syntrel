import discord
from discord.ext import commands
from discord.ext.commands import Context
import asyncio

# Make a pr to add your own server config here, you shouldn't need to touch the rest of the file, please fill in all the values for your own server
STICKY_CONFIGS = {
    "neotest": {
        "guild_id": 1069946178659160076,
        "channel_ids": [
            1455338488546459789,
        ],
        "allowed_role_id": 1432165329483857940,
        "message": "# Example sticky message",  # You can add your own markdown here
        "footer": "This is an automated sticky message.",  # This will be appended to the message and uses "-#" to format the footer
        "delay": 5,  # in seconds
    },
    "SideStore": {
        "guild_id": 949183273383395328,
        "channel_ids": [
            1279548738586673202,
        ],
        "allowed_role_id": 949207813815697479,
        "message": "## Please read the README in https://discord.com/channels/949183273383395328/1155736594679083089 and the documentation at <https://docs.sidestore.io> before asking your question.",
        "footer": "This is an automated sticky message.",
        "delay": 5,
    },
}


def has_allowed_role():
    async def predicate(context: Context):
        if not context.guild:
            context.bot.logger.warning(
                f"[STICKYBOT] Unauthorized stickybot command attempt by {context.author} ({context.author.id}) in DMs"
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
                f"[STICKYBOT] Unauthorized stickybot command attempt by {context.author} ({context.author.id}) in {context.guild.name} - no roles"
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

        for config in STICKY_CONFIGS.values():
            if context.guild.id != config.get("guild_id"):
                continue

            allowed_role_id = config.get("allowed_role_id")
            if allowed_role_id:
                allowed_role = context.guild.get_role(allowed_role_id)
                if allowed_role:
                    for role in context.author.roles:
                        if (
                            role.position >= allowed_role.position
                            and role.id != context.guild.default_role.id
                        ):
                            return True

        context.bot.logger.warning(
            f"[STICKYBOT] Unauthorized stickybot command attempt by {context.author} ({context.author.id}) in {context.guild.name} - insufficient role permissions"
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


def stickybot_command():
    async def wrapper(self, context: Context):
        embed = discord.Embed(
            title="Sticky Bot",
            description="Manages sticky messages in configured channels.",
            color=0x7289DA,
        )
        embed.set_author(
            name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png"
        )

        found_config = False
        if STICKY_CONFIGS:
            for name, config in STICKY_CONFIGS.items():
                guild_id = config.get("guild_id")
                if context.guild and guild_id == context.guild.id:
                    channel_ids = config.get("channel_ids", [])

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

                    allowed_role_id = config.get("allowed_role_id", "Not set")
                    role = context.guild.get_role(allowed_role_id)
                    role_display = (
                        f"<@&{allowed_role_id}> (`{allowed_role_id}`)"
                        if role
                        else f"`{allowed_role_id}`"
                    )

                    message_content = config.get("message", "*No message set*")
                    footer_text = config.get("footer", "This is an automated sticky message.")
                    full_content = f"{message_content}\n-# {footer_text}"

                    embed.add_field(
                        name="\u200b",
                        value=f"**Channels:**\n{channels_text}\n\n**Allowed Role:**\n{role_display}\n\n**Message Preview:**\n```\n{full_content}\n```",
                        inline=False,
                    )
                    found_config = True

        if not found_config:
            embed.add_field(
                name="No Configurations",
                value="No sticky configurations found for this server",
                inline=False,
            )

        if context.guild and context.guild.icon:
            embed.set_thumbnail(url=context.guild.icon.url)

        await context.send(embed=embed)

    return wrapper


class StickyBotListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_sticky_messages = {}
        self.debounce_tasks = {}

    async def delete_last_sticky(self, channel):
        try:
            active_config = None
            for config in STICKY_CONFIGS.values():
                if channel.guild.id == config.get(
                    "guild_id"
                ) and channel.id in config.get("channel_ids", []):
                    active_config = config
                    break

            if not active_config:
                return

            target_footer = active_config.get(
                "footer", "This is an automated sticky message."
            )

            async for message in channel.history(limit=20):
                if (
                    message.author.id == self.bot.user.id
                    and target_footer in message.content
                ):
                    await message.delete()
        except Exception as e:
            self.bot.logger.warning(
                f"[STICKYBOT] Error cleaning up sticky in #{channel.name}: {e}"
            )

    async def send_sticky_message(self, channel, config):
        if not channel:
            return

        last_msg_id = self.last_sticky_messages.get(channel.id)
        deleted = False
        if last_msg_id:
            try:
                old_msg = await channel.fetch_message(last_msg_id)
                await old_msg.delete()
                deleted = True
            except discord.NotFound:
                deleted = True
            except discord.Forbidden:
                self.bot.logger.warning(
                    f"[STICKYBOT] Missing delete permissions in #{channel.name}"
                )
            except Exception as e:
                self.bot.logger.warning(
                    f"[STICKYBOT] Error deleting info in #{channel.name}: {e}"
                )

        if not deleted:
            await self.delete_last_sticky(channel)

        message_content = config.get("message")
        if not message_content:
            return

        footer_text = config.get("footer", "This is an automated sticky message.")
        footer = f"\n-# {footer_text}"
        full_content = f"{message_content}{footer}"

        try:
            new_msg = await channel.send(
                full_content, allowed_mentions=discord.AllowedMentions.none()
            )
            self.last_sticky_messages[channel.id] = new_msg.id
        except discord.Forbidden:
            self.bot.logger.warning(
                f"[STICKYBOT] Missing send permissions in #{channel.name}"
            )
        except Exception as e:
            self.bot.logger.error(
                f"[STICKYBOT] Error sending sticky in #{channel.name}: {e}"
            )

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.initialize_stickies()

    async def initialize_stickies(self):
        for name, config in STICKY_CONFIGS.items():
            guild_id = config.get("guild_id")
            guild = self.bot.get_guild(guild_id)
            if not guild:
                continue

            channel_ids = config.get("channel_ids", [])
            for channel_id in channel_ids:
                channel = guild.get_channel(channel_id)
                if channel:
                    await self.send_sticky_message(channel, config)

    async def trigger_sticky(self, channel, guild):
        if not guild or not channel:
            return

        active_config = None
        for config in STICKY_CONFIGS.values():
            if guild.id == config.get("guild_id"):
                if channel.id in config.get("channel_ids", []):
                    active_config = config
                    break

        if not active_config:
            return

        channel_id = channel.id

        if channel_id in self.debounce_tasks:
            self.debounce_tasks[channel_id].cancel()

        async def debounce_wrapper():
            try:
                delay = active_config.get("delay", 5)
                await asyncio.sleep(delay)
                await self.send_sticky_message(channel, active_config)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.bot.logger.error(f"[STICKYBOT] Error in debounce task: {e}")
            finally:
                if self.debounce_tasks.get(channel_id) == asyncio.current_task():
                    del self.debounce_tasks[channel_id]

        self.debounce_tasks[channel_id] = self.bot.loop.create_task(debounce_wrapper())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        if message.id == self.last_sticky_messages.get(message.channel.id):
            return

        await self.trigger_sticky(message.channel, message.guild)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.user.bot:
            return

        if interaction.type == discord.InteractionType.application_command:
            await self.trigger_sticky(interaction.channel, interaction.guild)
