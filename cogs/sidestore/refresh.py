import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def refresh_command():
    @commands.hybrid_command(
        name="refresh", description="Help with refreshing or installing apps"
    )
    async def refresh(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# Can't Refresh or Install Apps\n\n---\n\n"
                + "1. Make sure your device is connected to a stable Wi-Fi network and not using cellular data.\n"
                + "2. Verify VPN is connected in the StosVPN app.\n"
                + "3. **Create a brand new pairing file.**\n"
                + "   - If none of the above worked, it is very likely that the pairing file is corrupted. You can reference the documentation on how to create a new pairing file [here](https://docs.sidestore.io/docs/installation/pairing-file).\n"
            ),
        )
        embed.set_author(
            name="SideStore",
            icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
        )
        embed.set_footer(text=f"Last Edited by neoarz")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/refresh.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/installation/pairing-file",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return refresh
