import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .livecontainer import LivecontainerView
from .jit26 import jit26_command


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Livecontainer(commands.GroupCog, name="livecontainer"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="livecontainer", invoke_without_command=True)
    async def livecontainer_group(self, context: Context):
        embed = discord.Embed(
            title="LiveContainer Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x0169FF,
        )
        embed.set_author(
            name="LiveContainer", icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png"
        )
        view = LivecontainerView(self.bot)
        await context.send(embed=embed, view=view)

    @livecontainer_group.command(name="help")
    async def livecontainer_group_help(self, context: Context):
        embed = discord.Embed(
            title="LiveContainer Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x0169FF,
        )
        embed.set_author(
            name="LiveContainer", icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png"
        )
        view = LivecontainerView(self.bot)
        await context.send(embed=embed, view=view)

    @livecontainer_group.command(name="26jit")
    async def livecontainer_group_26jit(self, context: Context):
        await self._invoke_hybrid(context, "26jit")

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown LiveContainer command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @app_commands.command(name="help", description="LiveContainer troubleshooting help")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="LiveContainer Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x0169FF,
        )
        embed.set_author(
            name="LiveContainer", icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png"
        )
        view = LivecontainerView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="26jit", description="26JIT information"
    )
    async def jit26(self, context):
        return await jit26_command()(self, context)


async def setup(bot) -> None:
    cog = Livecontainer(bot)
    await bot.add_cog(cog)

    bot.logger.info("Loaded extension 'livecontainer.help'")
    bot.logger.info("Loaded extension 'livecontainer.26jit'")

