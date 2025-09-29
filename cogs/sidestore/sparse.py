import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def sparse_command():
    @commands.hybrid_command(
        name="sparse", description="Information about SparseRestore exploit"
    )
    async def sparse(self, context):
        embed = discord.Embed(
            color=0x8e82f9,
            description=(
                '# SparseRestore "Bypass 3 App Limit" Exploit\n\n---\n\n' +
                'The SparseRestore exploit allows you to bypass the 3-app sideloading limit. It is compatible with iOS/iPadOS versions **15.2 to 18.1 beta 4**, (not including **17.7.1** and **17.7.2**).\n\n' +
                'iOS/iPadOS versions **17.0** (not including **16.7** and **16.7.10**) are recommended to use [Trollstore](https://ios.cfw.guide/installing-trollstore/)\n\n' +
                'If you\'re on a supported version and want to sideload more than three apps, follow the detailed instructions found in our documentation'
            )
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/sparse.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Documentation",
            style=discord.ButtonStyle.primary,
            url="https://docs.sidestore.io/docs/advanced/sparserestore",
            emoji="<:sidestorepride:1417717648795631787>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return sparse
