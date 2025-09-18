import discord
from discord import Interaction

from .views.base import BaseCog
from .views.models import AsyncTagManager, Tag
from .views.tags import ConfirmDeleteTag


class TagDelete:
    def __init__(self, cog: BaseCog):
        self.cog = cog

    async def check_conn_tag(self, name: str) -> str | Tag:
        if self.cog._conn is None:
            return "Error: couldn't connect to the db file to get tags!"
        if not name.isnumeric():
            return f"Error: Tag {name!r} was not found!"
        if (tag := await self.cog._conn.tag(tid=int(name))) is None:
            return f"Error: Tag with id {name!r} was not found!"
        return tag

    async def delete(self, inter: Interaction, name: str):
        """Delete a tag."""
        tag = await self.check_conn_tag(name)
        if isinstance(tag, str) or self.cog._conn is None:
            return await inter.response.send_message(tag, ephemeral=True)
        delete_tag = ConfirmDeleteTag(self.cog, tag)
        embed = discord.Embed(
            title="Confirm Deletion",
            description=f"Are you sure you want to delete `{tag.name}`?",
            color=0xFF0000
        )
        embed.set_author(name="Tags", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        await inter.response.send_message(
            embed=embed,
            view=delete_tag,
            ephemeral=True,
        )
