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
from utils import ascii, setup_logger, get_uptime, setup_signal_handlers

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




logger = setup_logger()


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")),
            intents=intents,
            help_command=None,
        )
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
        cogs_path = f"{os.path.realpath(os.path.dirname(__file__))}/cogs"
        disabled_env = os.getenv("DISABLED_COGS", "")
        disabled_cogs = {entry.strip().lower() for entry in disabled_env.split(",") if entry.strip()}
        
        for folder in os.listdir(cogs_path):
            folder_path = os.path.join(cogs_path, folder)
            if os.path.isdir(folder_path) and not folder.startswith('__'):
                init_file = os.path.join(folder_path, "__init__.py")
                if os.path.exists(init_file):
                    try:
                        await self.load_extension(f"cogs.{folder}")
                        if folder not in ["owner"]:
                            self.logger.info(f"Loaded extension '{folder}'")
                    except Exception as e:
                        exception = f"{type(e).__name__}: {e}"
                        self.logger.error(
                            f"Failed to load extension {folder}\n{exception}"
                        )
                else:
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
        statuses = ["SideStore", "MeloNX", "ARMSX2", "StikDebug", "Feather"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
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
        return get_uptime(self.start_time)

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
        if message.author == self.user or message.author.bot:
            return
        
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
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        
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
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error


bot = DiscordBot()

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(ascii)
    
    setup_signal_handlers(bot)
    
    try:
        bot.run(os.getenv("TOKEN"))
    except KeyboardInterrupt:
        pass
    except:
        pass
