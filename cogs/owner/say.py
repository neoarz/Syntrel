import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils.checks import is_owner_or_friend


class Say(commands.Cog, name="say"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def send_embed(self, context: Context, embed: discord.Embed, *, ephemeral: bool = False, allowed_mentions: discord.AllowedMentions = None) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral, allowed_mentions=allowed_mentions)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral, allowed_mentions=allowed_mentions)
        else:
            await context.send(embed=embed, allowed_mentions=allowed_mentions)

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(message="The message that should be repeated by the bot")
    @is_owner_or_friend()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        if context.guild is not None:
            self.bot.logger.info(
                f"Say command used in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id}): {message}"
            )
        else:
            self.bot.logger.info(
                f"Say command used in DMs by {context.author} (ID: {context.author.id}): {message}"
            )
        
        allowed_mentions = discord.AllowedMentions.none()
        
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            await interaction.response.defer(ephemeral=True)
            await context.channel.send(message, allowed_mentions=allowed_mentions)
            try:
                await interaction.delete_original_response()
            except:
                pass
        else:
            try:
                await context.message.delete()
            except:
                pass
            await context.send(message, allowed_mentions=allowed_mentions)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(message="The message that should be repeated by the bot")
    @is_owner_or_friend()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        if context.guild is not None:
            self.bot.logger.info(
                f"Embed command used in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id}): {message}"
            )
        else:
            self.bot.logger.info(
                f"Embed command used in DMs by {context.author} (ID: {context.author.id}): {message}"
            )
        
        allowed_mentions = discord.AllowedMentions.none()
        embed = discord.Embed(
            title="Say",
            description=message,
            color=0x7289DA,
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            await interaction.response.defer(ephemeral=True)
            await context.channel.send(embed=embed, allowed_mentions=allowed_mentions)
            try:
                await interaction.delete_original_response()
            except:
                pass
        else:
            try:
                await context.message.delete()
            except:
                pass
            await context.send(embed=embed, allowed_mentions=allowed_mentions)


    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, (commands.NotOwner, commands.CheckFailure)):
            embed = discord.Embed(
                title="Permission Denied",
                description="You are not the owner of this bot!",
                color=0xE02B2B,
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed, ephemeral=True)
        else:
            raise error


async def setup(bot) -> None:
    await bot.add_cog(Say(bot))
