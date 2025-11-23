import discord
from discord.ext import commands


def server_command():
    @commands.hybrid_command(
        name="server", description="Help with anisette server issues"
    )
    async def server(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# SideStore Freezing or Displaying an Error Code During Sign-In\n\n---\n\n"
                + "1. **Change the Anisette Server:**\n"
                + "   The most common solution is to switch to a different Anisette server. Do this:\n"
                + "   - Open Sidestore settings\n"
                + '   - Scroll down to the "Anisette Server" option\n'
                + "   - Select a different server from the list\n"
                + "   - You might need to try a few servers from the list and find which works best for you\n\n"
                + "2. **Host Your Own Anisette Server:**\n"
                + "   If you prefer, you can set up your own Anisette server. Detailed instructions for hosting an Anisette server are available in the official documentation and can be found [here](https://docs.sidestore.io/docs/advanced/anisette).\n\n"
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
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/server.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io/docs/troubleshooting/#sidestore-freezing-or-displaying-an-error-code-during-sign-in",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return server
