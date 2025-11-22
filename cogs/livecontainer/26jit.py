import discord
from discord.ext.commands import Context


def jit26_command():
    async def command(self, context: Context):
        embed = discord.Embed(
            title="Hello World",
            description="hello world",
            color=0x0169FF,
        )
        embed.set_author(
            name="26JIT", icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png"
        )
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)

    return command

