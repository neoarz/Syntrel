import discord
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import io


def piracy_command():
    @commands.hybrid_command(
        name="piracy",
        description="FBI Anti Piracy Warning",
    )
    async def piracy(self, context):
        image_url = "https://yes.nighty.works/raw/lEhuWK.png"

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                data = await resp.read()
        file = discord.File(io.BytesIO(data), filename="piracy.png")

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(file=file, ephemeral=False)
            else:
                await inter.followup.send(file=file, ephemeral=True)
        else:
            await context.send(file=file)

    return piracy
