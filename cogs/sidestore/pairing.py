import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def pairing_command():
    @commands.hybrid_command(
        name="pairing", description="Help with pairing file issues"
    )
    async def pairing(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# Cannot Choose Pairing File\n\n---\n\n"
                + "1. **Check File Extension:**\n"
                + "   Make sure your pairing file's extension ends with `.mobiledevicepairing` or `.plist`\n"
                + "   - If it doesn't, double-check to see if you had zipped your pairing file before sending it to your phone. Failing to do so may lead to the file being corrupted during transport\n\n"
                + "2. **Move Pairing File:**\n"
                + "   If you are unable to select the pairing file from within the app:\n"
                + "   - Rename the file to `ALTPairingFile.mobiledevicepairing`\n"
                + '   - Try moving the pairing file to the root directory of the SideStore folder in the Files app under "On My iPhone/iPad"\n\n'
                + "3. **Certificate Signing:**\n"
                + "   When signing SideStore with certain certificates, you won't be able to select the pairing file from within the app\n"
                + "   - Try the fix mentioned above\n"
                + "   - If you do not see the SideStore folder in the Files app:\n"
                + "     • Connect your phone to your computer\n"
                + "     • Drag and drop the pairing file into the SideStore app's files section\n"
                + "     • Ensure the file is renamed to `ALTPairingFile.mobiledevicepairing`\n"
            ),
        )
        embed.set_author(
            name="SideStore",
            icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
        )
        embed.set_footer(text=f"Last Edited by CelloSerenity")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/pairing.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/troubleshooting/#cannot-choose-pairing-file",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return pairing
