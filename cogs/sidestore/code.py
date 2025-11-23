import discord
from discord.ext import commands


def code_command():
    @commands.hybrid_command(
        name="code", description="No code received when signing in with Apple ID"
    )
    async def code(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "## Verification Code Not Received When Signing In with Apple ID\n\n---\n\n"
                + "1. **For iOS versions below 18.1:**\n"
                + '   - Open the "Settings" app\n'
                + "   - Tap on your name at the top of the screen\n"
                + '   - Navigate to "Sign-In and Security"\n'
                + '   - Select "Two-Factor Authentication"\n'
                + '   - Choose "Get Verification Code"\n\n'
                + "2. **For iOS versions 18.1 and above:**\n"
                + "   - Visit [iCloud](https://www.icloud.com) on a web browser\n"
                + '   - Click "Sign In"\n'
                + '   - On an Apple device, you may see two options: "Sign In" and "Use Different Apple Account"\n'
                + '   - Select the bottom option, "Use Different Apple Account"\n'
                + "   - Enter your Apple ID and password, DO NOT USE A PASSKEY\n"
                + "   - Apple will send you a verification code\n"
                + "   - Use this code in SideStore to complete the sign-in process\n"
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
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/code.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/troubleshooting/#sign-in-issues",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return code
