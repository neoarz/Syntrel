import os
import signal
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Shutdown(commands.Cog, name="shutdown"):
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

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        # Log command execution before shutdown starts
        if context.guild is not None:
            self.bot.logger.info(
                f"Executed shutdown command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.bot.logger.info(
                f"Executed shutdown command by {context.author} (ID: {context.author.id}) in DMs"
            )

        embed = discord.Embed(
            title="Shutdown",
            description="Shutting down. Bye! <a:PandaThanos:1417483671253811262>",
            color=0x7289DA,
        ).set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")

        await self.send_embed(context, embed)
        os.kill(os.getpid(), signal.SIGTERM)

    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.NotOwner):
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
    await bot.add_cog(Shutdown(bot))
