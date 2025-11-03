import discord
from discord.ext import commands


def upgrade_command():
    @commands.hybrid_command(
        name="upgrade", description="How can I upgrade my firmware and keys in MeloNX?"
    )
    async def upgrade(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                "# How can I upgrade my firmware and keys in MeloNX?\n\n---\n\n"
                + "First, dump **BOTH** the firmware and keys from a **MODDED SWITCH**.\n\n"
                + "## Keys:\n"
                + "1. Go to the root folder of MeloNX in the files app.\n"
                + '2. Open the "system" folder.\n'
                + '3. Delete the "prod.keys" and "title.keys".\n\n'
                + "## Firmware:\n"
                + "1. Go to the root folder of MeloNX in the files app.\n"
                + '2. Open the "bis" folder.\n'
                + '3. Open the "system" folder.\n'
                + '4. Delete the "Contents" folder.\n\n'
                + "## Lastly:\n"
                + "1. Go to MeloNX's advanced tab in settings.\n"
                + '2. Select the "Show Setup Screen" option.\n\n'
                + "You will now be able to import your new keys and firmware."
            ),
        )
        embed.set_author(
            name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
        )
        embed.set_footer(text="Last Edited by Meshal :D")
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/upgrade.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="MeloNX Discord",
                style=discord.ButtonStyle.primary,
                url="https://discord.gg/EMXB2XYQgA",
                emoji="<:Discord:1428762057758474280>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return upgrade

