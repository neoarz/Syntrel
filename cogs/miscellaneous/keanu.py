import discord
from discord.ext import commands
from discord.ext.commands import Context
import random


class Keanu(commands.Cog, name="keanu"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="keanu",
        description="Reeves",
    )
    async def keanu(self, context: Context) -> None:
        images = [
            "https://yes.nighty.works/raw/z0HqUM.png",
            "https://yes.nighty.works/raw/1Jc0j6.avif",
            "https://yes.nighty.works/raw/uQyDyg.webp",
            "https://yes.nighty.works/raw/LzrPZz.png",
            "https://yes.nighty.works/raw/BZgKzR.jpg",
            "https://yes.nighty.works/raw/xOzCta.jpg",
            "https://yes.nighty.works/raw/eWvQa5.webp",
            "https://yes.nighty.works/raw/Qg9HJr.webp",
            "https://yes.nighty.works/raw/tYfOEn.webp",
            "https://yes.nighty.works/raw/kZS1Mu.jpg",
            "https://yes.nighty.works/raw/E83And.png",
            "https://yes.nighty.works/raw/PRr6ln.jpg",
            "https://yes.nighty.works/raw/ZlprB5.jpg",
            "https://yes.nighty.works/raw/BvcXOg.jpg",
            "https://yes.nighty.works/raw/C7gy4v.jpg",
            "https://yes.nighty.works/raw/XqHg1q.jpg",
            "https://yes.nighty.works/raw/RUXNK7.png",
            "https://yes.nighty.works/raw/CBNs9L.jpg"
        ]
        
        embed = discord.Embed(
            description="## Reeves",
            color=0x7289DA,
        )
        embed.set_author(name="Keanu", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.set_image(url=random.choice(images))
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
