import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


class Code(commands.Cog, name="code"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="code", description="No code received when signing in with Apple ID"
    )
    async def code(self, context: Context) -> None:
        embed = discord.Embed(
            color=0x8e82f9,
            description=(
                '## Verification Code Not Received When Signing In with Apple ID\n\n---\n\n' +
                
                '1. **For iOS versions below 18.1:**\n' +
                '   - Open the "Settings" app\n' +
                '   - Tap on your name at the top of the screen\n' +
                '   - Navigate to "Sign-In and Security"\n' +
                '   - Select "Two-Factor Authentication"\n' +
                '   - Choose "Get Verification Code"\n\n' +
                '2. **For iOS versions 18.1 and above:**\n' +
                '   - Visit [iCloud](https://www.icloud.com) on a web browser\n' +
                '   - Click "Sign In"\n' +
                '   - When prompted, you will see two options: "Sign In" and "Use Different Apple Account"\n' +
                '   - Select the bottom option, "Use Different Apple Account"\n' +
                '   - Enter your Apple ID and password\n' +
                '   - Apple will send you a verification code\n' +
                '   - Use this code in Sidestore to complete the sign-in process\n' 
            )
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        embed.set_footer(text=f'Last Edited by neoarz')
        embed.timestamp = discord.utils.utcnow()
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command", 
            style=discord.ButtonStyle.secondary, 
            url="https://github.com/neoarz/syntrel/blob/main/cogs/sidestore/code.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        view.add_item(discord.ui.Button(
            label="Documentation", 
            style=discord.ButtonStyle.primary, 
            url="https://docs.sidestore.io/docs/troubleshooting/#sign-in-issues",
            emoji="<:sidestorepride:1417717648795631787>"
        ))

        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Code(bot))
