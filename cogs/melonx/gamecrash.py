import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def crash_command():
    @commands.hybrid_command(
        name="gamecrash", description="Why does my game crash?"
    )
    async def crash(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                '# "Why does my game crash?"\n\n---\n\n' +
                '**This can be caused by multiple reasons:**\n' +
                '- Not enough available ram\n' +
                '- You may have tried to update your firmware without updating your keys\n' +
                '- Game file is corrupted/broken\n' +
                '- Game requires a higher firmware+keys combination than you currently have\n' +
                '- In rare cases some games also crash when not having the resolution set to 1x\n' +
                '- The a12 chipset have a lot of issues at the moment\n' +
                '- Shader cache isn\'t cleared after updating MeloNX\n' +
                '- iOS 15 and 16 are known to have some compatibility issues'
            )
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/gamecrash.py",
            emoji="<:githubicon:1417717356846776340>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return crash
