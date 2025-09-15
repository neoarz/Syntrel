import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context


class RandomFact(commands.Cog, name="randomfact"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        title="Random Fact",
                        description=data["text"], 
                        color=0x7289DA
                    )
                    embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                    embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
                await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(RandomFact(bot))