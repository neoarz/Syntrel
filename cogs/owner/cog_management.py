import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class CogManagement(commands.Cog, name="cog_management"):
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
            await self.send_embed(context, embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Could not load the `{cog}` cog.\n```{str(e)}```", color=0xE02B2B
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed, ephemeral=True)
            return
        embed = discord.Embed(
            description=f"Successfully loaded the `{cog}` cog.", color=0xBEBEFE
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        await self.send_embed(context, embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Could not unload the `{cog}` cog.\n```{str(e)}```", color=0xE02B2B
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed, ephemeral=True)
            return
        embed = discord.Embed(
            description=f"Successfully unloaded the `{cog}` cog.", color=0xBEBEFE
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        await self.send_embed(context, embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Could not reload the `{cog}` cog.\n```{str(e)}```", color=0xE02B2B
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed, ephemeral=True)
            return
        embed = discord.Embed(
            title="Cog Management",
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        await self.send_embed(context, embed)

    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error",
                description="You are not the owner of the bot!",
                color=0xE02B2B
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed, ephemeral=True)
        else:
            raise error


async def setup(bot) -> None:
    await bot.add_cog(CogManagement(bot))
