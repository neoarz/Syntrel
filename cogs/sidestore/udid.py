import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def udid_command():
    @commands.hybrid_command(
        name="udid", description="SideStore could not determine device UDID"
    )
    async def udid(self, context):
        embed = discord.Embed(
            color=0x8e82f9,
            description=(
                '# SideStore Could Not Determine Device UDID\n\n---\n\n' +
                'This error usually occurs when the pairing file is corrupted. Please create a new pairing file using `idevice_pair` and try again.\n\n' +
                'If you forgot how to generate a new pairing file, you can refer to the documentation below.'
            )
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/udid.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Documentation",
            style=discord.ButtonStyle.secondary,
            url="https://docs.sidestore.io/docs/installation/pairing-file/",
            emoji="<:sidestorepride:1417717648795631787>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return udid
