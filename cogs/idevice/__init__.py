import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .idevice import ideviceView
from .error_codes import errorcodes_command
from .developermode import developermode_command
from .noapps import noapps_command
from .mountddi import mountddi_command

class Idevice(commands.GroupCog, name="idevice"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="idevice", invoke_without_command=True)
    async def idevice_group(self, context: Context):
        embed = discord.Embed(
            title="idevice Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0xfa8c4a
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        view = ideviceView(self.bot)
        await context.send(embed=embed, view=view)

    @idevice_group.command(name="help")
    async def idevice_group_help(self, context: Context):
        embed = discord.Embed(
            title="idevice Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0xfa8c4a
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        view = ideviceView(self.bot)
        await context.send(embed=embed, view=view)

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown idevice command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @idevice_group.command(name="errorcodes")
    async def idevice_group_errorcodes(self, context: Context):
        await self._invoke_hybrid(context, "errorcodes")

    @idevice_group.command(name="developermode")
    async def idevice_group_developermode(self, context: Context):
        await self._invoke_hybrid(context, "developermode")

    @idevice_group.command(name="noapps")
    async def idevice_group_noapps(self, context: Context):
        await self._invoke_hybrid(context, "noapps")

    @idevice_group.command(name="mountddi")
    async def idevice_group_mountddi(self, context: Context):
        await self._invoke_hybrid(context, "mountddi")

    @app_commands.command(
        name="help",
        description="idevice troubleshooting help"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="idevice Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0xfa8c4a
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        view = ideviceView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="errorcodes",
        description="Look up error codes and their meanings."
    )
    async def errorcodes(self, context, *, error_code: str = None):
        return await errorcodes_command()(self, context, error_code=error_code)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="developermode",
        description="How to turn on developer mode"
    )
    async def developermode(self, context):
        return await developermode_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="noapps",
        description="Help when apps aren't showing in installed apps view"
    )
    async def noapps(self, context):
        return await noapps_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="mountddi",
        description="How to manually mount DDI"
    )
    async def mountddi(self, context):
        return await mountddi_command()(self, context)

async def setup(bot) -> None:
    cog = Idevice(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'idevice.help'")
    bot.logger.info("Loaded extension 'idevice.errorcodes'")
    bot.logger.info("Loaded extension 'idevice.developermode'")
    bot.logger.info("Loaded extension 'idevice.noapps'")
    bot.logger.info("Loaded extension 'idevice.mountddi'")
