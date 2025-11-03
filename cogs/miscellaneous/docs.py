import discord
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import io


def docs_command():
    @commands.hybrid_command(name="docs", description="Shows the docs image.")
    async def docs(self, context):
        url = "https://yes.nighty.works/raw/akdx0q.webp"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()
        file = discord.File(io.BytesIO(data), filename="docs.webp")

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(
                    "## Dont be like the rest, read the docs",
                    file=file,
                    ephemeral=False,
                )
            else:
                await inter.followup.send(
                    "## Dont be like the rest, read the docs", file=file, ephemeral=True
                )
        else:
            await context.send("## Dont be like the rest, read the docs", file=file)

    return docs
