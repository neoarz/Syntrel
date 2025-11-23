import discord
from discord.ext import commands
import aiohttp
import io


def support_command():
    @commands.hybrid_command(name="support", description="Shows the support image.")
    async def support(self, context):
        url = "https://yes.nighty.works/raw/wGzHIV.gif"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()
        file = discord.File(io.BytesIO(data), filename="support.gif")

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(file=file, ephemeral=False)
            else:
                await inter.followup.send(file=file, ephemeral=True)
        else:
            await context.send(file=file)

    return support
