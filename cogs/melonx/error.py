import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def error_command():
    @commands.hybrid_command(
        name="error", description="What does this error message mean?"
    )
    async def error(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                '# What does this error message mean?\n\n---\n\n' +
                '**1. "MeloNX Crashed! System.SystemException: Cannot allocate memory"**' +
                'You likely don\'t have the increased memory limit entitlement enabled, are using an a12 chipset, and have 4GB or less of memory. You can see the status of the entitlement for MeloNX under the Settings tab.\n\n' +
                '**2. "MeloNX Crashed! LibHac.Common.HorizonResultException: ResultLoaderInvalidNso (2009-0005)"**' +
                'This is likely a bad game / update / or DLC dump. redump your files and try again.'
            )
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/error.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Join The MeloNX Discord Server", 
            style=discord.ButtonStyle.primary, 
            url="https://discord.gg/WEX6mUbq5c",
            emoji="<:discord:1428671438071791736>>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return error
