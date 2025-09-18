from discord import Interaction

from .views.base import BaseCog
from .views.models import AsyncTagManager, Tag
from .views.tags import TagEmbed, TagButtonView


class TagSend:
    def __init__(self, cog: BaseCog):
        self.cog = cog
        
    @property
    def conn(self) -> AsyncTagManager:
        return self.cog.conn

    async def check_conn_tag(self, name: str) -> str | Tag:
        if self.cog._conn is None:
            return "Error: couldn't connect to the db file to get tags!"
        if not name.isnumeric():
            return f"Error: Tag {name!r} was not found!"
        if (tag := await self.cog._conn.tag(tid=int(name))) is None:
            return f"Error: Tag with id {name!r} was not found!"
        return tag

    async def send(self, inter: Interaction, name: str):
        """Send contents of a tag."""
        tag = await self.check_conn_tag(name)
        if isinstance(tag, str) or self.cog._conn is None:
            return await inter.response.send_message(tag, ephemeral=True)
        ephemeral = inter.guild is None
        author = self.cog.bot.get_user(tag.author)
        authname = author.name if author else str(tag.author)
        await inter.response.send_message(
            embeds=[TagEmbed(tag, authname)],
            view=TagButtonView(tag.buttons),
            ephemeral=ephemeral
        )
        tag.used += 1
        await self.cog._conn.update(tag)
        self.cog.logger.info(f"{inter.user.name!r} sent {tag.name!r}")
