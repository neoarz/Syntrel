import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


class Half(commands.Cog, name="half"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="half", description="Help when apps get stuck installing"
    )
    async def half(self, context: Context) -> None:
        embed = discord.Embed(
            color=0x8e82f9,
            description=(
                '# Sidestore/IPAs Stuck Halfway Through Installing or Refreshing\n\n---\n' +
                '### Method 1: Basic Troubleshooting\n\n' +
                '- Restart SideStore\n' +
                '- Restart device\n' +
                '- Clear Cache\n' +
                '- Change Anisette Server\n' +
                '- Reset adi.pb\n' +
                '- Sign out from SideStore and sign back in\n' +
                '- Regenerate pairing file\n' +
                '- Reinstall SideStore\n\n' +
                '### Method 2: If Method 1 Doesn\'t Work\n\n' +
                '1. Delete Sidestore\n' +
                '2. Reinstall SideStore using the guide at https://docs.sidestore.io/\n' +
                '3. **Do not use the IPA provided by the website**, instead use this older version: [Sidestore 0.5.9 download](https://github.com/SideStore/SideStore/releases/download/0.5.9/SideStore.ipa)\n' +
                '4. Setup SideStore and StosVPN as usual\n' +
                '> -# Step 3 is the important one (make sure to do that)\n'
            )
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/neos-helper-bot/blob/main/cogs/sidestore/half.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Documentation",
            style=discord.ButtonStyle.primary,
            url="https://docs.sidestore.io/docs/troubleshooting/common-issues#sidestore-hangs-halfway-through-installation",
            emoji="<:sidestorepride:1417717648795631787>"
        ))

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Half(bot))
