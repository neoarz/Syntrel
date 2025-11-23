import discord
from discord.ext.commands import Context


def jit26_command():
    async def command(self, context: Context):
        embed = discord.Embed(
            color=0x0169FF,
            description=(
                "# iOS 26 JIT & Sideloading Walkthrough\n\n---\n\n"
                "Click the [button below](https://github.com/CelloSerenity/iOS-26-Sideloading-and-JIT-Complete-Walkthrough) to get started with iOS 26 JIT and sideloading."
            ),
        )
        embed.set_author(
            name="LiveContainer",
            icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png",
        )
        embed.set_footer(
            icon_url="https://yes.nighty.works/raw/2PPWd3.webp",
            text="Made By CelloSerenity",
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Get Started",
                url="https://github.com/CelloSerenity/iOS-26-Sideloading-and-JIT-Complete-Walkthrough",
                style=discord.ButtonStyle.primary,
                emoji="<:githubicon:1417717356846776340>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return command
