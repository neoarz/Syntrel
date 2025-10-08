import discord
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import io


def rr_command():
    @commands.hybrid_command(
        name="rr",
        description="Rickroll",
    )
    async def rr(self, context):
        gif_url = "https://yes.nighty.works/raw/JzjMcs.gif"

        async with aiohttp.ClientSession() as session:
            async with session.get(gif_url) as resp:
                data = await resp.read()
        file = discord.File(io.BytesIO(data), filename="rickroll.gif")

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(file=file, ephemeral=False)
            else:
                await inter.followup.send(file=file, ephemeral=True)
        else:
            await context.send(file=file)
    
    return rr
