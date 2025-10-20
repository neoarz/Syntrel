import aiohttp
import discord
from discord.ext import commands

def randomfact_command():
    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context):
        embed = discord.Embed(
            title="Command Disabled",
            description="This command is currently disabled.",
            color=0xE02B2B,
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        await context.send(embed=embed)
    
    return randomfact
