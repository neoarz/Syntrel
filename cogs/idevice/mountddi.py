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
                "# How to Mount your DDI (Developer Disk Image):\n\n---\n\n"
                "1. Ensure you are connected to StikDebug's VPN and Wi-Fi.*\n"
                "2. Force close StikDebug from the app switcher, then repon it.*\n"
                "## This should resolve your error! Remember, this must be done every time you restart your device.:*\n"
                "If it doesn't work after a couple tries or you live in a country where github.com is blocked, try the steps below to manually mount the DDI:*\n"
                "1. **Download the DDI.zip file attached above:**\n"
                "   - Save it to your device and extract the contents\n\n"
                "2. **Replace the DDI folder in StikDebug:**\n"
                "   - Navigate to the StikDebug default directory on your iPhone/iPad\n"
                "   - Delete the existing DDI folder completely\n"
                "   - Replace it with the DDI folder from uncompressing the downloaded zip\n"
                "   - Make sure it's in StikDebug's default directory\n\n"
                "3. **Restart and retry:**\n"
                "   - Completely restart StikDebug\n"
                "   - If you still get the same error, ask the idevice server for more help\n\n"
            ),
        )
        embed.set_author(
            name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png"
        )
        embed.set_footer(text="Last Edited by CelloSerenity")
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
