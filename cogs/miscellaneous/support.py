import discord
from discord.ext import commands
from discord.ext.commands import Context

def support_command():
    @commands.hybrid_command(
        name="support",
        description="Shows the support image."
    )
    async def support(self, context):
        embed = discord.Embed(
            color=0x7289DA
        )
        embed.set_author(name="Support", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.set_image(url="https://yes.nighty.works/raw/X8XeCV.png")
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return support
