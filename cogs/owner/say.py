import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Say(commands.Cog, name="say"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def send_embed(self, context: Context, embed: discord.Embed, *, ephemeral: bool = False) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(
            title="Say",
            description=message,
            color=0x7289DA,
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        await self.send_embed(context, embed)


    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.NotOwner):
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
