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
                "# SideStore Could Not Determine Device UDID\n\n--- For iOS 26.4 ---\n\n"
                + "1. Open Settings, click General, click VPN & Device Management, click your email developer apps, delete them all."
                + "2. Open iLoader, scroll down, click Delete Stored Pairing."
                + "3. Scroll back up, click Refresh."
                + "4. Pair your idevice with iLoader."
                + "5. Click SideStore (Stable)"
                + "6. Open SideStore when it's done installing"
                + "7. Refresh SideStore to see if everything is working"
                + "8. If Step #7 does not work, reboot your idevice"
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
