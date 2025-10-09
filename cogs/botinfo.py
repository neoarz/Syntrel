import platform
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class BotInfo(commands.Cog, name="botinfo"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def botinfo(self, context: Context) -> None:
        embed = discord.Embed(
            title="Syntrel Discord Bot",
            color=0x7289DA,
        )
        embed.set_author(name="Bot Information", icon_url="https://yes.nighty.works/raw/gSxqzV.png")
        embed.add_field(name="Owner:", value="[neoarz](https://discordapp.com/users/1015372540937502851)", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.bot_prefix} for normal commands",
            inline=False,
        )
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(BotInfo(bot))
