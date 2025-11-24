import discord
from discord.ext import commands


def afc_command():
    @commands.hybrid_command(
        name="afc", description="Help with AFC Connection Failure issues"
    )
    async def afc(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# AFC Connection Failure\n\n---\n\n"
                + "1. Make sure Wi-Fi is connected to a stable network\n"
                + "2. Make sure StosVPN is connected and updated\n"
                + "3. If issue still persists, replace pairing file using `iloader`. See [Pairing File instructions](https://docs.sidestore.io/docs/advanced/pairing-file) for details"
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
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/afc.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/troubleshooting/common-issues#afc-connection-failure",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return afc
