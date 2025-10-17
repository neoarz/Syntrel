import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def mods_command():
    @commands.hybrid_command(
        name="mods", description="How to install mods within MeloNX (Limited Support)"
    )
    async def mods(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                '# How do I install mods within MeloNX? (Limited Support)\n\n---\n\n' +
                '### **romFS/exeFS mods**:\n' +
                '1. Obtain your title ID of your game by copying it from MeloNX, Hold down on the game and click game info.\n' +
                '2. Copy it and then go to Files-> MeloNX-> mods-> contents\n' +
                '3. In the contents folder create a new folder and name it the title ID you copied earlier.\n' +
                '4. Now place all your mods for that game in the folder you just made (these should be folders with the mod name, do not mess with the file structure of the mod after unzipping it.)\n\n' +
                '### **Atmosphere mods**: \n' +
                '1. Obtain your title ID of your game by copying it from MeloNX, Hold down on the game and click game info.\n' +
                '2. Copy it and then go to Files-> MeloNX-> sdcard-> atmosphere-> contents\n' +
                '3. In the contents folder create a new folder and name it the title ID you copied earlier.\n' +
                '4. Now place all your mods for that game in the folder you just made (these should be folders with the mod name, do not mess with the file structure of the mod after unzipping it.)'
            )
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/mods.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="MeloNX Discord", 
            style=discord.ButtonStyle.primary, 
            url="https://discord.gg/EMXB2XYQgA",
            emoji="<:Discord:1428762057758474280>"
        ))
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


    return mods
