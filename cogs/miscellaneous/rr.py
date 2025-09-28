import discord
from discord.ext import commands
from discord.ext.commands import Context


class Rr(commands.Cog, name="rr"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="rr",
        description="Rickroll",
    )
    async def rr(self, context: Context) -> None:
        gif_url = "https://yes.nighty.works/raw/JzjMcs.gif"
        
        embed = discord.Embed(
            color=0x7289DA,
        )
        embed.set_author(name="Rickroll", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.set_image(url=gif_url)
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Rr(bot))
