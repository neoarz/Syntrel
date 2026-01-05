import discord
from discord.ext import commands


def unofficial_command():
    @commands.hybrid_command(
        name="unofficial", description="Unofficial guides and video walkthroughs"
    )
    async def unofficial(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "# Unofficial Guides and Videos\n\n---\n\n"
                + "**PLEASE ONLY READ THE OFFICIAL DOCUMENTATION AND TROUBLESHOOTING GUIDE LOCATED AT https://docs.sidestore.io**\n\n"
                + "If you do not try this first we **WILL NOT** provide support.\n\n"
                + "There are currently **NO official video walkthroughs**."
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
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/sidestore/unofficial.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Documentation",
                style=discord.ButtonStyle.primary,
                url="https://docs.sidestore.io",
                emoji="<:sidestorepride:1417717648795631787>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return unofficial
