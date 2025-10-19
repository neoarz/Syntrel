import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


def transfer_command():
    @commands.hybrid_command(
        name="transfer", description="How to transfer save files from other emulators or platforms"
    )
    async def transfer(self, context):
        embed = discord.Embed(
            color=0x963155,
            description=(
                '# How do I transfer my save files from another emulator, my pc, or other platform?\n\n---\n\n' +
                '### **Ryujinx Based**: \n' +
                '1. Go too Ryujinx\'s main directory -> copy and and transfer the **"bis"** folder to your iDevice.\n' +
                '2. Replace the **"bis"** folder in MeloNX with the one you transferred over.\n\n' +
                '### **Yuzu Based**:\n' +
                '1. Go to Yuzu\'s main directory and locate "**nand**" then go to -> users -> save\n' +
                '2. Get the **title ID** of the game you want to transfer to by locating the game on MeloNX, hold down on it and press "Game Info" \n' +
                '3. Then search the title ID within the **save** folder\n' +
                '4. Open that folder labeled your title ID and copy of all of the contents to your iDevice\n' +
                '5. Boot the game once in MeloNX so the save directories appear and is the latest created\n' +
                '6. On your iDevice, go into files-> MeloNX -> bis -> user -> save\n' +
                '7. In the save folder, there will be many folders named 0000001, 0000002, etc\n' +
                '8. Sort by last modified or open each one too see the modified date/time of the files\n' +
                '9. Once you\'ve found the newest one, inside will be two folders named 1 and 0, one will have a brand new save file inside.\n' +
                '10. drop the contents copied from the title ID folder in Yuzu into that directory and press "replace" when prompted.\n' +
                '11. Launch the game again in MeloNX to verify the transfer.'
            )
        )
        embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
        embed.set_footer(text=f'Last Edited by Meshal :D')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/melonx/transfer.py",
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


    return transfer
