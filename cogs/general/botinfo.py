import platform
import discord
from discord.ext import commands
from discord.ext.commands import Context


class BotInfo(commands.Cog, name="botinfo"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="Nyrix Discord Bot",
            color=0x7289DA,
        )
        embed.set_author(name="Bot Information", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        embed.add_field(name="Owner:", value="[neoarz](https://discordapp.com/users/1015372540937502851)", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.bot_prefix} for normal commands",
            inline=False,
        )
        if getattr(context, "interaction", None):
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(BotInfo(bot))