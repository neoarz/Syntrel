import discord
from discord.ext import commands
import os


def mountddi_command():
    @commands.hybrid_command(name="mountddi", description="How to manually mount DDI")
    async def mountddi(self, context):
        await context.defer()

        embed = discord.Embed(
            color=0xFA8C4A,
            description=(
                "# How to Manually Mount DDI\n\n---\n\n"
                "1. **Download the DDI.zip file attached above:**\n"
                "   - Save it to your device and extract the contents\n\n"
                "2. **Replace the DDI folder in StikDebug:**\n"
                "   - Navigate to the StikDebug default directory on your iPhone/iPad\n"
                "   - Delete the existing DDI folder completely\n"
                "   - Replace it with the DDI folder from the downloaded zip\n"
                "   - Make sure it's in the StikDebug default directory\n\n"
                "3. **Restart and retry:**\n"
                "   - Completely restart StikDebug\n"
                "   - See if you get the same error again\n\n"
            ),
        )
        embed.set_author(
            name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png"
        )
        embed.set_footer(text="Last Edited by neoarz")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/idevice/mountddi.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )

        ddi_file_path = os.path.join(os.path.dirname(__file__), "files/DDI.zip")
        file = (
            discord.File(ddi_file_path, filename="DDI.zip")
            if os.path.exists(ddi_file_path)
            else None
        )

        if file:
            await context.send(embed=embed, view=view, file=file)
        else:
            await context.send(embed=embed, view=view)

    return mountddi
