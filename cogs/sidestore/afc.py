import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


class Afc(commands.Cog, name="afc"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="afc", description="Help with AFC Connection Failure issues"
    )
    async def afc(self, context: Context) -> None:
        embed = discord.Embed(
            color=0x8e82f9,
            description=(
                '# AFC Connection Failure\n\n---\n\n' +
                '1. Make sure StosVPN is connected\n' +
                '2. If issue still persists, generate and import a new pairing file using `idevice_pair`. See our [Pairing File instructions](https://docs.sidestore.io/docs/installation/pairing-file) for details'
            )
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/afc.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Documentation",
            style=discord.ButtonStyle.primary,
            url="https://docs.sidestore.io/docs/troubleshooting/common-issues#afc-connection-failure",
            emoji="<:sidestorepride:1417717648795631787>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Afc(bot))
