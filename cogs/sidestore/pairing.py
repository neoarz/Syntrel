import discord
from discord.ext import commands


def pairing_command():
    @commands.hybrid_command(
        name="pairing", description="Link to the pairing guide"
    )
    async def pairing(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# How to obtain your pairing file:\n\n---\n\n"
                + "[Click here](https://docs.sidestore.io/advanced/pairing-file) to read the SideStore documentation on replacing your pairing file.**\n"
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
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/pairing.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/advanced/pairing-file",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return pairing
