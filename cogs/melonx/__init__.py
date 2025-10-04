import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .melonx import MelonxView
from .transfer import transfer_command

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

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown MeloNX command: {name}")

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

    @commands.hybrid_command(
        name="transfer",
        description="How to transfer save files from other emulators or platforms"
    )
    async def transfer(self, context):
        return await transfer_command()(self, context)

async def setup(bot) -> None:
    cog = Melonx(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'melonx.help'")
    bot.logger.info("Loaded extension 'melonx.transfer'")
