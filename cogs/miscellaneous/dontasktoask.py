import discord
from discord.ext import commands
from discord.ext.commands import Context

def dontasktoask_command():
    @commands.hybrid_command(
        name="dontasktoask",
        description="Shows the 'Don't Ask to Ask' image."
    )
    async def dontasktoask(self, context):
        embed = discord.Embed(
            color=0x7289DA
        )
        embed.set_author(name="Don't Ask to Ask", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.set_image(url="https://yes.nighty.works/raw/KecbCr.jpg")
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return dontasktoask
