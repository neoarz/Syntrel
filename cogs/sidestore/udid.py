import discord
from discord.ext import commands


def udid_command():
    @commands.hybrid_command(
        name="udid", description="SideStore could not determine device UDID"
    )
    async def udid(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# SideStore Could Not Determine Device UDID\n\n"
                + "---\n\n"
                + "1. Open SideStore, click Settings, and click "Reset Pairing File".\n"
                + "2. Open iLoader, scroll down, click Delete Stored Pairing.\n"
                + "3. Scroll back up, click Refresh.\n"
                + "4. Pair your idevice with iLoader.\n"
                + "5. Click "Manage Pairing File".\n"
                + "6. Press "Place In All Apps".\n"
                + "7. Refresh SideStore to see if everything is working.\n"
                + "8. If Step #7 does not work, reboot your idevice.\n"
                + "9. If Step #8 does not work, read the documentation."
            ),
        )
        embed.set_author(
            name="SideStore",
            icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
        )
        embed.set_footer(text="Last Edited by Mr Saturn")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/udid.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.secondary,
                url="https://docs.sidestore.io/docs/troubleshooting/error-codes#1006-sidestore-could-not-determine-this-devices-udid",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return udid
