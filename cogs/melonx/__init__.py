import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .melonx import MelonxView
from .transfer import transfer_command
from .mods import mods_command
from .legal import legal_command
from .gamecrash import crash_command
from .requirements import requirements_command
from .error import error_command
from .ios26 import ios26_command


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Melonx(commands.GroupCog, name="melonx"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="melonx", invoke_without_command=True)
    async def melonx_group(self, context: Context):
        embed = discord.Embed(
            title="MeloNX Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x963155
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        view = MelonxView(self.bot)
        await context.send(embed=embed, view=view)

    @melonx_group.command(name="help")
    async def melonx_group_help(self, context: Context):
        embed = discord.Embed(
            title="MeloNX Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x963155
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        view = MelonxView(self.bot)
        await context.send(embed=embed, view=view)

    @melonx_group.command(name="transfer")
    async def melonx_group_transfer(self, context: Context):
        await self._invoke_hybrid(context, "transfer")

    @melonx_group.command(name="legal")
    async def melonx_group_legal(self, context: Context):
        await self._invoke_hybrid(context, "legal")

    @melonx_group.command(name="mods")
    async def melonx_group_mods(self, context: Context):
        await self._invoke_hybrid(context, "mods")

    @melonx_group.command(name="gamecrash")
    async def melonx_group_gamecrash(self, context: Context):
        await self._invoke_hybrid(context, "gamecrash")

    @melonx_group.command(name="requirements")
    async def melonx_group_requirements(self, context: Context):
        await self._invoke_hybrid(context, "requirements")

    @melonx_group.command(name="error")
    async def melonx_group_error(self, context: Context):
        await self._invoke_hybrid(context, "error")

    @melonx_group.command(name="26")
    async def melonx_group_26(self, context: Context):
        await self._invoke_hybrid(context, "26")

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown MeloNX command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @app_commands.command(
        name="help",
        description="MeloNX troubleshooting help"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="MeloNX Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x963155
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        view = MelonxView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="transfer",
        description="How to transfer save files from other emulators or platforms"
    )
    async def transfer(self, context):
        return await transfer_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="mods",
        description="How to install mods within MeloNX (Limited Support)"
    )
    async def mods(self, context):
        return await mods_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="legal",
        description="Legality of emulators"
    )
    async def legal(self, context):
        return await legal_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="gamecrash",
        description="Why does my game crash?"
    )
    async def gamecrash(self, context):
        return await crash_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="requirements",
        description="What does MeloNX require?"
    )
    async def requirements(self, context):
        return await requirements_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="error",
        description="What does this error message mean?"
    )
    async def error(self, context):
        return await error_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="26",
        description="How can I run MeloNX on iOS 26?"
    )
    async def ios26(self, context):
        return await ios26_command()(self, context)

async def setup(bot) -> None:
    cog = Melonx(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'melonx.help'")
    bot.logger.info("Loaded extension 'melonx.transfer'")
    bot.logger.info("Loaded extension 'melonx.mods'")
    bot.logger.info("Loaded extension 'melonx.gamecrash'")
    bot.logger.info("Loaded extension 'melonx.requirements'")
    bot.logger.info("Loaded extension 'melonx.error'")
    bot.logger.info("Loaded extension 'melonx.26'")
    bot.logger.info("Loaded extension 'melonx.legal'")
