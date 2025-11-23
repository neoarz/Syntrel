import discord
from discord.ext import commands


def crash_command():
    @commands.hybrid_command(
        name="crash", description="Help with SideStore crashing issues"
    )
    async def crash(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# SideStore Crashing After Refresh\n\n---\n\n"
                + "First, to try and save your data:\n"
                + "1. DON'T DELETE SIDESTORE, reinstall with AltServer's `Sideload .ipa`.\n"
                + "If that doesn't work:\n"
                + "1. Delete your current SideStore. Reinstall with AltServer.\n"
                + "2. Import your pairing file and sign into SideStore.\n"
                + "3. Download the SideStore .ipa file, and save it to your Files app.\n"
                + '4. Import the "Sidestore.ipa" file into SideStore, just like how you import any other IPA.\n\n'
                + "This process ensures SideStore is refreshed without issues."
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
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/crash.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return crash
