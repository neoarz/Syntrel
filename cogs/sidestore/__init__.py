import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .sidestore import SidestoreView
from .refresh import refresh_command
from .code import code_command
from .crash import crash_command
from .pairing import pairing_command
from .server import server_command
from .afc import afc_command
from .udid import udid_command
from .half import half_command
from .sparse import sparse_command


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Sidestore(commands.GroupCog, name="sidestore"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="sidestore", invoke_without_command=True)
    async def sidestore_group(self, context: Context):
        embed = discord.Embed(
            title="SideStore Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x8e82f9
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        view = SidestoreView(self.bot)
        await context.send(embed=embed, view=view)

    @sidestore_group.command(name="help")
    async def sidestore_group_help(self, context: Context):
        embed = discord.Embed(
            title="SideStore Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x8e82f9
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        view = SidestoreView(self.bot)
        await context.send(embed=embed, view=view)

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown SideStore command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @sidestore_group.command(name="refresh")
    async def sidestore_group_refresh(self, context: Context):
        await self._invoke_hybrid(context, "refresh")

    @sidestore_group.command(name="code")
    async def sidestore_group_code(self, context: Context):
        await self._invoke_hybrid(context, "code")

    @sidestore_group.command(name="crash")
    async def sidestore_group_crash(self, context: Context):
        await self._invoke_hybrid(context, "crash")

    @sidestore_group.command(name="pairing")
    async def sidestore_group_pairing(self, context: Context):
        await self._invoke_hybrid(context, "pairing")

    @sidestore_group.command(name="server")
    async def sidestore_group_server(self, context: Context):
        await self._invoke_hybrid(context, "server")

    @sidestore_group.command(name="afc")
    async def sidestore_group_afc(self, context: Context):
        await self._invoke_hybrid(context, "afc")

    @sidestore_group.command(name="udid")
    async def sidestore_group_udid(self, context: Context):
        await self._invoke_hybrid(context, "udid")

    @sidestore_group.command(name="half")
    async def sidestore_group_half(self, context: Context):
        await self._invoke_hybrid(context, "half")

    @sidestore_group.command(name="sparse")
    async def sidestore_group_sparse(self, context: Context):
        await self._invoke_hybrid(context, "sparse")

    @app_commands.command(
        name="help",
        description="SideStore troubleshooting help"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="SideStore Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x8e82f9
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")

        view = SidestoreView(self.bot)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="refresh",
        description="Help with refreshing or installing apps"
    )
    async def refresh(self, context):
        return await refresh_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="code",
        description="No code received when signing in with Apple ID"
    )
    async def code(self, context):
        return await code_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="crash",
        description="Help with SideStore crashing issues"
    )
    async def crash(self, context):
        return await crash_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="pairing",
        description="Help with pairing file issues"
    )
    async def pairing(self, context):
        return await pairing_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="server",
        description="Help with anisette server issues"
    )
    async def server(self, context):
        return await server_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="afc",
        description="Help with AFC Connection Failure issues"
    )
    async def afc(self, context):
        return await afc_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="udid",
        description="SideStore could not determine device UDID"
    )
    async def udid(self, context):
        return await udid_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="half",
        description="Help with half-installed apps"
    )
    async def half(self, context):
        return await half_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="sparse",
        description="Help with sparse bundle issues"
    )
    async def sparse(self, context):
        return await sparse_command()(self, context)

async def setup(bot) -> None:
    cog = Sidestore(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'sidestore.help'")
    bot.logger.info("Loaded extension 'sidestore.refresh'")
    bot.logger.info("Loaded extension 'sidestore.code'")
    bot.logger.info("Loaded extension 'sidestore.crash'")
    bot.logger.info("Loaded extension 'sidestore.pairing'")
    bot.logger.info("Loaded extension 'sidestore.server'")
    bot.logger.info("Loaded extension 'sidestore.afc'")
    bot.logger.info("Loaded extension 'sidestore.udid'")
    bot.logger.info("Loaded extension 'sidestore.half'")
    bot.logger.info("Loaded extension 'sidestore.sparse'")
