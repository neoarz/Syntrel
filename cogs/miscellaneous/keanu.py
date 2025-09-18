import discord
from discord.ext import commands
from discord.ext.commands import Context


class Keanu(commands.Cog, name="keanu"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="keanu",
        description="Reeves",
    )
    async def keanu(self, context: Context) -> None:
        embed = discord.Embed(
            description="## Reeves",
            color=0x7289DA,
        )
        embed.set_author(name="Keanu", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.set_image(url="https://yes.nighty.works/raw/JqDYPJ.avif")
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Keanu(bot))
