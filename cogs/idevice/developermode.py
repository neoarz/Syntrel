import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def developermode_command():
    @commands.hybrid_command(
        name="developermode", description="How to turn on developer mode"
    )
    async def developermode(self, context):
        embed = discord.Embed(
            color=0xFA8C4A,
            description=(
                "# How to Enable Developer Mode\n\n---\n\n"
                + '1. Open the "Settings" app\n'
                + '2. Navigate to "Privacy & Security"\n'
                + '3. Scroll all the way down to find "Developer Mode"\n\n'
                + "If you don't see the Developer Mode option, you need to install a developer app first.\n\n"
                + "You can use [SideStore](https://sidestore.io/) for this purpose - follow their installation guide to get started."
            ),
        )
        embed.set_author(
            name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png"
        )
        embed.set_footer(text=f"Last Edited by neoarz")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/idevice/developermode.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return developermode
