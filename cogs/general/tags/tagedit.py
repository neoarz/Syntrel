from discord import Interaction, Embed

from .views.base import BaseCog
from .views.models import AsyncTagManager, Tag
from .views.tags import EditTagPreview


class TagEdit:
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

    async def edit(self, inter: Interaction, name: str):
        """Edit a tag."""
        tag = await self.check_conn_tag(name)
        if isinstance(tag, str) or self.cog._conn is None:
            return await inter.response.send_message(tag, ephemeral=True)
        
        embed = Embed(
            title=f"Edit Tag: {tag.name}",
            description=f"```\n{tag.content}\n```",
            color=0x7289DA
        )
        embed.set_author(name="Tags", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        embed.set_footer(text="Click Edit to modify this tag or Close to cancel")
        
        view = EditTagPreview(self.cog, tag)
        await inter.response.send_message(embed=embed, view=view, ephemeral=True)
