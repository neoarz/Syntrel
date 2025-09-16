import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Sync(commands.Cog, name="sync"):
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

    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """
        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                title="Sync",
                description="Slash commands have been globally synchronized.",
                color=0x7289DA,
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                title="Sync",
                description="Slash commands have been synchronized in this guild.",
                color=0x7289DA,
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed)
            return
        embed = discord.Embed(
            title="Error",
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B,
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        await self.send_embed(context, embed, ephemeral=True)

    @commands.command(
        name="unsync",
        description="Unsynchonizes the slash commands.",
    )
    @app_commands.describe(
        scope="The scope of the sync. Can be `global`, `current_guild` or `guild`"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """
        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                title="Unsync",
                description="Slash commands have been globally unsynchronized.",
                color=0x7289DA,
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                title="Unsync",
                description="Slash commands have been unsynchronized in this guild.",
                color=0x7289DA,
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed)
            return
        embed = discord.Embed(
            title="Error",
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B,
        )
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        await self.send_embed(context, embed, ephemeral=True)


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
    await bot.add_cog(Sync(bot))
