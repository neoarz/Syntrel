import discord
from discord.ext import commands
from discord.ext.commands import Context


def jit26_command():
    async def command(self, context: Context):
        embed = discord.Embed(
            title="Hello World",
            description="hello world",
            color=0x0169FF,
        )
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)

    return command

