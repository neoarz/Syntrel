import discord
from discord.ext import commands
from discord.ext.commands import Context
import asyncio
from datetime import datetime, timedelta

# Make a pr to add your own server config here, you shouldn't need to touch the rest of the file
BAIT_CONFIGS = {
    "SideStore": {
        "guild_id": 949183273383395328,
        "channel_id": 1432149872953262151,
        "protected_role_id": 123456789123456789,
    },
    "neotest": {
        "guild_id": 1069946178659160076,
        "channel_id": 1432149872953262151,
        "protected_role_id": 1432165329483857940,
    },
}

BAN_REASON = 'Detected bot/scammer in bait channel'

def has_protected_role():
    async def predicate(context: Context):
        if not context.guild:
            embed = discord.Embed(
                title="Permission Denied",
                description="You don't have permission to use this command.",
                color=0xE02B2B
            )
            embed.set_author(name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png")
            await context.send(embed=embed, ephemeral=True)
            return False
        
        if not hasattr(context.author, 'roles'):
            embed = discord.Embed(
                title="Permission Denied",
                description="You don't have permission to use this command.",
                color=0xE02B2B
            )
            embed.set_author(name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png")
            await context.send(embed=embed, ephemeral=True)
            return False
        
        for config in BAIT_CONFIGS.values():
            protected_role_id = config.get("protected_role_id")
            if protected_role_id:
                protected_role = context.guild.get_role(protected_role_id)
                if protected_role:
                    for role in context.author.roles:
                        if role.position >= protected_role.position and role.id != context.guild.default_role.id:
                            return True
        
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xE02B2B
        )
        embed.set_author(name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png")
        await context.send(embed=embed, ephemeral=True)
        return False
    return commands.check(predicate)

def baitbot_command():
    async def wrapper(self, context: Context):
        embed = discord.Embed(
            title="Bait Bot Configuration",
            description="Bans people who post in a specific channel.\n\n"
                       "**Configuration:**",
            color=0x7289DA
        )
        embed.set_author(name="Events", icon_url="https://yes.nighty.works/raw/C8Hh6o.png")

        found_config = False
        if BAIT_CONFIGS:
            for name, config in BAIT_CONFIGS.items():
                guild_id = config.get("guild_id")
                if context.guild and guild_id == context.guild.id:
                    channel_id = config.get("channel_id", "Not set")
                    role_id = config.get("protected_role_id", "Not set")

                    server_name = context.guild.name

                    channel = context.guild.get_channel(channel_id)
                    channel_display = f"<#{channel_id}> (`{channel_id}`)" if channel else f"`{channel_id}`"

                    role = context.guild.get_role(role_id)
                    role_display = f"<@&{role_id}> (`{role_id}`)" if role else f"`{role_id}`"

                    embed.add_field(
                        name=server_name,
                        value=f"Channel: {channel_display}\nProtected Role: {role_display}",
                        inline=False
                    )
                    found_config = True

        if not found_config:
            embed.add_field(
                name="No Configurations",
                value="No bait channels configured for this server",
                inline=False
            )

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
            if message.channel.id == config.get("channel_id") and message.guild.id == config.get("guild_id"):
                bait_config = config
                config_name = name
                break
        
        if not bait_config:
            return
        
        protected_role_id = bait_config.get("protected_role_id")
        if protected_role_id and hasattr(message.author, 'roles'):
            protected_role = message.guild.get_role(protected_role_id)
            if protected_role:
                for role in message.author.roles:
                    if role.position >= protected_role.position and role.id != message.guild.default_role.id:
                        return
        
        try:
            self.bot.logger.warning(f'[BAITBOT] Detected user in bait channel [{config_name}]: {message.author.name} ({message.author.id}) in #{message.channel.name}')
            
            await message.author.ban(reason=BAN_REASON, delete_message_days=7)
            self.bot.logger.info(f'[BAITBOT] Banned {message.author.name} - deleted messages from last 7 days')
            
            await asyncio.sleep(2)
            await message.guild.unban(message.author, reason="Auto-unban after cleanup")
            self.bot.logger.info(f'[BAITBOT] Unbanned {message.author.name} - cleanup complete')
            
        except discord.Forbidden:
            self.bot.logger.error(f'[BAITBOT] No permission to ban {message.author.name}')
        except Exception as e:
            self.bot.logger.error(f'[BAITBOT] Error handling bait message: {e}')
