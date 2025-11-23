import discord
from discord.ext import commands
import aiohttp
import io


def dontasktoask_command():
    @commands.hybrid_command(
        name="dontasktoask", description="Shows the 'Don't Ask to Ask' image."
    )
    async def dontasktoask(self, context):
        image_url = "https://yes.nighty.works/raw/KecbCr.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                data = await resp.read()
        file = discord.File(io.BytesIO(data), filename="dontasktoask.jpg")

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(file=file, ephemeral=False)
            else:
                await inter.followup.send(file=file, ephemeral=True)
        else:
            await context.send(file=file)

    return dontasktoask
