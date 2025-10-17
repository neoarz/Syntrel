import discord
from discord.ext import commands
from discord.ext.commands import Context


def silly_command():
    @commands.hybrid_command(
        name="silly",
        description="Sends a silly message :3",
    )
    async def silly(self, context, message_type: str = "regular"):
        if message_type == "animated":
            message = "https://yes.nighty.works/raw/LX4nqt.gif"
        else:
            message = ":3"
            
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            await interaction.response.defer(ephemeral=True)
            await context.channel.send(message)
            try:
                await interaction.delete_original_response()
            except:
                pass
        else:
            try:
                await context.message.delete()
            except:
                pass
            await context.channel.send(message)
    
    return silly