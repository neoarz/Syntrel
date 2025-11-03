import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def requirements_command():
    @commands.hybrid_command(
        name="requirements", description="What does MeloNX require?"
    )
    async def requirements(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                '# "What does MeloNX require?"\n\n---\n\n'
                + "- JIT is **Mandatory**, because of this MeloNX will never be on the App Store / TestFlight\n"
                + "- A Modded Nintendo Switch\n"
                + "- The Increased Memory Limit Entitlement\n"
                + "- A device with a **A12/M1** chip and **4GB Ram** or higher\n"
                + "- TrollStore is supported with limited functionality for iOS 15"
            ),
        )
        embed.set_author(
            name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
        )
        embed.set_footer(text=f"Last Edited by Meshal :D")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/requirements.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="MeloNX Discord",
                style=discord.ButtonStyle.primary,
                url="https://discord.gg/EMXB2XYQgA",
                emoji="<:Discord:1428762057758474280>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return requirements
