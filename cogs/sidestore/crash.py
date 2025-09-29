import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def crash_command():
    @commands.hybrid_command(
        name="crash", description="Help with SideStore crashing issues"
    )
    async def crash(self, context):
        embed = discord.Embed(
            color=0x8e82f9,
            description=(
                '# Sidestore Crashing After Refresh\n\n---\n\n' +
                '1. Delete your current SideStore.\n' +
                '2. Reinstall with AltServer.\n' +
                '3. Select the pairing file and sign into SideStore.\n' +
                '4. Download the SideStore .ipa file, and save it to your Files app.\n' +
                '5. Import the "Sidestore.ipa" file into SideStore, just like how you import any other IPA.\n\n' +
                'This process ensures SideStore is refreshed without issues.'
            )
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/crash.py",
            emoji="<:githubicon:1417717356846776340>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return crash
