import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time
import os


class Mountddi(commands.Cog, name="mountddi"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="mountddi", description="How to manually mount DDI"
    )
    async def mountddi(self, context: Context) -> None:
        embed = discord.Embed(
            color=0xfa8c4a,
            description=(
                '# How to Manually Mount DDI\n\n---\n\n' +
                '1. **Download the DDI.zip file attached above:**\n' +
                '   - Save it to your device and extract the contents\n\n' +
                '2. **Replace the DDI folder in StikDebug:**\n' +
                '   - Navigate to the StikDebug default directory on your iPhone/iPad\n' +
                '   - Delete the existing DDI folder completely\n' +
                '   - Replace it with the DDI folder from the downloaded zip\n' +
                '   - Make sure it\'s in the StikDebug default directory\n\n' +
                '3. **Restart and retry:**\n' +
                '   - Completely restart StikDebug\n' +
                '   - See if you get the same error again\n\n'
            )
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/idevice/mountddi.py",
            emoji="<:githubicon:1417717356846776340>"
        ))

        ddi_file_path = os.path.join(os.path.dirname(__file__), 'files/DDI.zip')
        
        try:
            if context.interaction:
                if os.path.exists(ddi_file_path):
                    file = discord.File(ddi_file_path, filename='DDI.zip')
                    await context.interaction.response.send_message(embed=embed, view=view, file=file)
                else:
                    await context.interaction.response.send_message(embed=embed, view=view)
            else:
                if os.path.exists(ddi_file_path):
                    file = discord.File(ddi_file_path, filename='DDI.zip')
                    await context.send(embed=embed, view=view, file=file)
                else:
                    await context.send(embed=embed, view=view)
        except discord.NotFound:
            if context.interaction:
                await context.interaction.followup.send(embed=embed, view=view)
            else:
                await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Mountddi(bot))
