import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def ios26_command():
    @commands.hybrid_command(
        name="26", description="How can I run MeloNX on iOS 26?"
    )
    async def ios26(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                '# "How can I run MeloNX on iOS 26?"\n\n---\n\n' +
                '### StikDebug\n' +
                '1. Make sure StikDebug is on the latest version.\n' +
                '2. Turn on "Picture in Picture" in StikDebug\'s settings.\n\n' +
                '### MeloNX\n' +
                'Make sure you\'re on the latest public beta.\n' +
                'https://discord.com/channels/1300369899704680479/1412931489817034892\n\n' +
                '## Disclaimer:\n\n' +
                'If you\'re on iOS 18 or below, and emulation is essential to you:\n\n' +
                '## <:error:1424007141768822824> DO NOT UPDATE <:error:1424007141768822824> \n\n' +
                'iOS 26 has many issues related to emulation.'
            )
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/ios26.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Join The MeloNX Discord Server", 
            style=discord.ButtonStyle.primary, 
            url="https://discord.gg/WEX6mUbq5c",
            emoji="<:discord:1428671438071791736>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return ios26
