import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


class Noapps(commands.Cog, name="noapps"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="noapps", description="Help when apps aren't showing in installed apps view"
    )
    async def noapps(self, context: Context) -> None:
        embed = discord.Embed(
            color=0xfa8c4a,
            description=(
                '# Apps Not Showing in Installed Apps View\n\n---\n\n' +
                'If apps aren\'t appearing in the StikDebug installed apps view, this is likely because they were signed with a distribution certificate instead of a development certificate.\n\n' +
                'Distribution certificates lack the `get-task-allow` entitlement needed for JIT.\n\n' +
                'To fix this issue:\n' +
                '- Use a development certificate when signing apps, or\n' +
                '- Try SideStore, the best free sideloading method available\n\n' +
                'More details can be found at [SideStore\'s official website](https://sidestore.io/)'
            )
        )
        embed.set_author(name="iDevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/idevice/noapps.py",
            emoji="<:githubicon:1417717356846776340>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Noapps(bot))
