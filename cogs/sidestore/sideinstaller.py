import discord
from discord.ext import commands


def sideinstaller_command():
    @commands.hybrid_command(
        name="sideinstaller", description="Warn about SideInstaller issues"
    )
    async def sideinstaller(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description=(
                "We will not help you solve any issues encountered due to the use of SideInstaller, "
                "as it is not affiliated with the SideStore team."
            ),
        )
        embed.set_author(
            name="SideStore",
            icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
        )
        embed.timestamp = discord.utils.utcnow()

        if context.interaction:
            await context.interaction.response.send_message(embed=embed)
        else:
            await context.send(embed=embed)

    return sideinstaller
