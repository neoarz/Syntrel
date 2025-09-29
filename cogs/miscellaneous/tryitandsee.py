import discord
from discord.ext import commands
from discord.ext.commands import Context


def tryitandsee_command():
    @commands.hybrid_command(
        name="tryitandsee",
        description="Try it and see",
    )
    async def tryitandsee(self, context):
        gif_url = "https://yes.nighty.works/raw/1BQP8c.gif"
        
        embed = discord.Embed(
            color=0x7289DA,
        )
        embed.set_author(name="Try It And See", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.set_image(url=gif_url)
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return tryitandsee
