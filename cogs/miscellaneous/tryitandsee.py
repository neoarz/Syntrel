import discord
from discord.ext import commands
from discord.ext.commands import Context


def tryitandsee_command():
    @commands.hybrid_command(
        name="tryitandsee",
        description="Try it and see",
    )
    async def tryitandsee(self, context):
        link = "https://tryitands.ee/"
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(link, ephemeral=False)
            else:
                await inter.followup.send(link, ephemeral=True)
        else:
            await context.send(link)
    
    return tryitandsee
