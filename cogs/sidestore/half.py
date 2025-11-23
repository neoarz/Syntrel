import discord
from discord.ext import commands


def half_command():
    @commands.hybrid_command(
        name="half", description="Help when apps get stuck installing"
    )
    async def half(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# SideStore/IPAs Stuck Halfway Through Installing or Refreshing\n\n---\n"
                + "- Make sure you are on the latest version of SideStore\n"
                + "- Restart SideStore\n"
                + "- Restart device\n"
                + "- Clear Cache\n"
                + "- Change Anisette Server\n"
                + "- Reset adi.pb\n"
                + "- Sign out from SideStore and sign back in\n"
                + "- Recreate pairing file\n"
                + "- Reinstall SideStore\n\n"
            ),
        )
        embed.set_author(
            name="SideStore",
            icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
        )
        embed.set_footer(text="Last Edited by CelloSerenity")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/half.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/troubleshooting/common-issues#sidestore-hangs-halfway-through-installation",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return half
