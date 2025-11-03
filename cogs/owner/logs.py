import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils.ascii_art import ascii_plain
from utils.checks import is_owner_or_friend


class Logs(commands.Cog, name="logs"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def send_embed(
        self, context: Context, embed: discord.Embed, *, ephemeral: bool = False
    ) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(
                    embed=embed, ephemeral=ephemeral
                )
        else:
            await context.send(embed=embed)

    async def send_file(
        self, context: Context, *, file: discord.File, ephemeral: bool = False
    ) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(file=file, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(file=file, ephemeral=ephemeral)
        else:
            await context.send(file=file)

    @commands.hybrid_command(
        name="logs",
        description="View the bot's log file",
    )
    @app_commands.describe(
        lines="Number of lines to read from the end of the log file (default: 50, max: 200)"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @is_owner_or_friend()
    async def logs(self, context: Context, lines: int = 50) -> None:
        if lines > 200:
            lines = 200
        elif lines < 1:
            lines = 1

        log_file_path = os.getenv("LOG_FILE", "logs/discord.log")

        if not os.path.isabs(log_file_path):
            log_file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                log_file_path,
            )

        try:
            if not os.path.exists(log_file_path):
                embed = discord.Embed(
                    title="Error",
                    description=f"Log file not found at: `{log_file_path}`",
                    color=0xE02B2B,
                )
                embed.set_author(
                    name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp"
                )
                await self.send_embed(context, embed, ephemeral=True)
                return

            with open(log_file_path, "r", encoding="utf-8", errors="replace") as f:
                all_lines = f.readlines()

            if not all_lines:
                embed = discord.Embed(
                    title="Logs",
                    description="Log file is empty.",
                    color=0x7289DA,
                )
                embed.set_author(
                    name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp"
                )
                await self.send_embed(context, embed, ephemeral=True)
                return

            selected_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            log_content = "".join(selected_lines)

            log_file = f"logs.txt"
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(
                    f"Bot logs extracted at {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
                )
                f.write(
                    f"Last {len(selected_lines)} lines from {os.path.basename(log_file_path)}\n"
                )
                f.write(f"Total lines in log file: {len(all_lines)}\n")
                f.write("-" * 50 + "\n\n")
                f.write(ascii_plain + "\n\n")
                f.write(log_content)

            file_obj = discord.File(log_file)
            await self.send_file(context, file=file_obj, ephemeral=True)

            os.remove(log_file)

        except PermissionError:
            embed = discord.Embed(
                title="Error",
                description=f"Permission denied when trying to read log file: `{log_file_path}`",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp"
            )
            await self.send_embed(context, embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while reading the log file:\n```\n{str(e)}\n```",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp"
            )
            await self.send_embed(context, embed, ephemeral=True)

    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, (commands.NotOwner, commands.CheckFailure)):
            embed = discord.Embed(
                title="Permission Denied",
                description="You are not the owner of this bot!",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp"
            )
            await self.send_embed(context, embed, ephemeral=True)
        else:
            raise error


async def setup(bot) -> None:
    await bot.add_cog(Logs(bot))
