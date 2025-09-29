import discord
from discord.ext import commands
from discord.ext.commands import Context


def piracy_command():
    @commands.hybrid_command(
        name="piracy",
        description="FBI Anti Piracy Warning",
    )
    async def piracy(self, context):
        embed = discord.Embed(
            color=0xE02B2B,
        )
        embed.set_author(name="Piracy", icon_url="https://yes.nighty.works/raw/rVYXlf.png")
        embed.set_image(url="https://yes.nighty.works/raw/lEhuWK.png")
        embed.set_footer(text="FBI Anti Piracy Warning", icon_url="https://yes.nighty.works/raw/8qjzP3.png")
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return piracy
