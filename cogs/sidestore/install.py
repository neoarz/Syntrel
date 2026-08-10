import discord
from discord.ext import commands


def install_command():
    @commands.hybrid_command(name="install", description="Install SideStore")
    async def install(self, context):
        embed = discord.Embed(
            color=0x8E82F9,
            description="You can install SideStore [here](https://sidestore.io).",
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

    return install
