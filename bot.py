import asyncio
import json
import logging
import os
import platform
import random
import signal
import sys
import time

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

from database import DatabaseManager

load_dotenv()

"""	
Default Intents:
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

intents.members = True
intents.presences = True
"""

intents = discord.Intents.default()
intents.message_content = True
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.messages = True 




class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")),
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The logger is available using the following code:
        - self.logger # In this class
        - bot.logger # In this file
        - self.bot.logger # In cogs
        """
        self.logger = logger
        self.database = None
        self.bot_prefix = os.getenv("PREFIX")
        self.invite_link = os.getenv("INVITE_LINK")
        self.start_time = time.time()
        self._shutdown = False

    async def init_db(self) -> None:
        async with aiosqlite.connect(
            f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
        ) as db:
            with open(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql",
                encoding = "utf-8"
            ) as file:
                await db.executescript(file.read())
            await db.commit()

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        cogs_path = f"{os.path.realpath(os.path.dirname(__file__))}/cogs"
        disabled_env = os.getenv("DISABLED_COGS", "")
        disabled_cogs = {entry.strip().lower() for entry in disabled_env.split(",") if entry.strip()}
        
        for folder in os.listdir(cogs_path):
            folder_path = os.path.join(cogs_path, folder)
            if os.path.isdir(folder_path) and not folder.startswith('__'):
                for file in os.listdir(folder_path):
                    if file.endswith(".py") and not file.startswith('__'):
                        extension = file[:-3]
                        full_name = f"{folder}.{extension}".lower()
                        if extension.lower() in disabled_cogs or full_name in disabled_cogs:
                            self.logger.info(f"Skipped disabled extension '{full_name}'")
                            continue
                        try:
                            await self.load_extension(f"cogs.{folder}.{extension}")
                            self.logger.info(f"Loaded extension '{folder}.{extension}'")
                        except Exception as e:
                            exception = f"{type(e).__name__}: {e}"
                            self.logger.error(
                                f"Failed to load extension {folder}.{extension}\n{exception}"
                            )
        
        for file in os.listdir(cogs_path):
            if file.endswith(".py") and not file.startswith('__'):
                extension = file[:-3]
                if extension.lower() in disabled_cogs:
                    self.logger.info(f"Skipped disabled extension '{extension}'")
                    continue
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["Sidestore", "MeloNX", "Armsx2", "Stikdebug", "Feather"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        
        try:
            app_info = await self.application_info()
            if app_info.team:
                self.logger.info(f"Bot owned by team: {app_info.team.name}")
                for member in app_info.team.members:
                    self.logger.info(f"Team member: {member.name} (ID: {member.id})")
            else:
                self.logger.info(f"Bot owner: {app_info.owner.name} (ID: {app_info.owner.id})")
        except Exception as e:
            self.logger.error(f"Error fetching application info: {e}")
            
        await self.init_db()
        await self.load_cogs()
        self.status_task.start()
        self.database = DatabaseManager(
            connection=await aiosqlite.connect(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
            )
        )

    def get_uptime(self) -> str:
        uptime_seconds = int(time.time() - self.start_time)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    async def close(self) -> None:
        if self._shutdown:
            return
        self._shutdown = True
        
        self.logger.info("Starting shutdown process...")
        
        if self.status_task and not self.status_task.is_being_cancelled():
            self.status_task.cancel()
            self.logger.info("Status task cancelled")
            
        if self.database and self.database.connection:
            try:
                await self.database.connection.close()
                self.logger.warning("Database connection closed")
            except Exception as e:
                self.logger.error(f"Error closing database connection: {e}")
            
        try:
            await super().close()
            self.logger.critical("Bot shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during bot shutdown: {e}")

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        
        # Reacts to messages which mention the bot
        if self.user in message.mentions:
            try:
                emoji_string = "<a:PandaPing:1417550314260926575>"
                self.logger.debug(f"Attempting to react with PandaPing emoji: {emoji_string}")
                await message.add_reaction(emoji_string)
                self.logger.debug("Successfully reacted with PandaPing emoji")
            except Exception as e:
                self.logger.debug(f"Failed to react with PandaPing emoji: {e}")
                try:
                    self.logger.debug("Falling back to wave emoji")
                    await message.add_reaction("👋")
                    self.logger.debug("Successfully reacted with wave emoji")
                except Exception as fallback_error:
                    self.logger.debug(f"Failed to react with fallback emoji: {fallback_error}")
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        
        # Skip logging for shutdown command as it logs manually before shutdown
        if executed_command.lower() == "shutdown":
            return
            
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandNotFound):
            if context.guild is not None:
                self.logger.info(
                    f"Unknown command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id}): {context.message.content}"
                )
            else:
                self.logger.info(
                    f"Unknown command in DMs by {context.author} (ID: {context.author.id}): {context.message.content}"
                )
            return
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error


def signal_handler(signum, frame):
    logger.info("Shutdown requested. Closing bot...")
    if bot.loop and not bot.loop.is_closed():
        asyncio.create_task(bot.close())
        bot.loop.call_soon_threadsafe(bot.loop.stop)


bot = DiscordBot()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        bot.run(os.getenv("TOKEN"))
    except KeyboardInterrupt:
        pass
    except:
        pass
