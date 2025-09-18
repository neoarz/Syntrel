from discord import Interaction, Embed, Color
from discord.ui import View
from discord.app_commands import Choice, Group, autocomplete, describe

from .views.base import BaseCog
from .views.models import AsyncTagManager, Tag
from .views.tags import (
    AddTagButtonModal,
    TagSelectButton,
)
from .tagsend import TagSend
from .tagcreate import TagCreate
from .tagedit import TagEdit
from .tagdelete import TagDelete


class Tags(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.description = "A cog for retrieving and setting tags."

        self._conn: AsyncTagManager | None = None
        
        # Initialize command classes
        self.tag_send = TagSend(self)
        self.tag_create = TagCreate(self)
        self.tag_edit = TagEdit(self)
        self.tag_delete = TagDelete(self)

    @property
    def conn(self) -> AsyncTagManager:
        if self._conn is None: raise ValueError("Initialized improperly!")
        return self._conn

    @classmethod
    async def setup(cls, bot):
        import os
        c = await super().setup(bot)
        db_path = f"{os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))}/database/database.db"
        c._conn = await AsyncTagManager.from_file(db_path)
        return c

    async def cog_unload(self):
        if self._conn:
            await self._conn.close()
        await super().cog_unload()

    async def tag_completer(self, inter: Interaction, current: str):
        _ = inter
        if self._conn is None or inter.guild is None:
            return []
        return [
            Choice(name=f"[G] {t.name}" if t.guild is None else t.name, value=str(t.tid))
            for t in await self._conn.tags
            if current.lower() in t.name.lower() and (inter.guild.id == t.guild or t.guild is None)
        ][:25]

    async def tag_button_completer(self, inter: Interaction, current: str):
        _ = inter
        if self._conn is None or inter.guild is None:
            return []
        return [
            Choice(name=f"[G] {t.name}" if t.guild is None else t.name, value=str(t.tid))
            for t in await self._conn.tags
            if current.lower() in t.name.lower()
            and (inter.guild.id == t.guild or t.guild is None)
            and len(t.buttons) > 0
        ][:25]

    tags = Group(name="tags", description="The parent for tag operations.", guild_only=True)
    urls = Group(name="urls", description="Manage url buttons for tags.", parent=tags, guild_only=True)

    async def check_conn_tag(self, name: str) -> str | Tag:
        if self._conn is None:
            return "Error: couldn't connect to the db file to get tags!"
        if not name.isnumeric():
            return f"Error: Tag {name!r} was not found!"
        if (tag := await self._conn.tag(tid=int(name))) is None:
            return f"Error: Tag with id {name!r} was not found!"
        return tag

    @tags.command(description="Send contents of a tag.")
    @describe(name="The name of the tag you want to send.")
    @autocomplete(name=tag_completer)
    async def send(self, inter: Interaction, name: str):
        await self.tag_send.send(inter, name)

    @tags.command(description="Create a new tag.")
    async def create(self, inter: Interaction):
        await self.tag_create.create(inter)

    @tags.command(description="Edit a tag.")
    @describe(name="The name of the tag you want to edit.")
    @autocomplete(name=tag_completer)
    async def edit(self, inter: Interaction, name: str):
        await self.tag_edit.edit(inter, name)

    @tags.command(description="Delete a tag.")
    @describe(name="The name of the tag you want to delete.")
    @autocomplete(name=tag_completer)
    async def delete(self, inter: Interaction, name: str):
        await self.tag_delete.delete(inter, name)

    @urls.command(name="add", description="Add a url button to tag.")
    @describe(name="The name of the tag you want to add a url button to.")
    @autocomplete(name=tag_completer)
    async def button_add(self, inter: Interaction, name: str):
        tag = await self.check_conn_tag(name)
        if isinstance(tag, str) or self._conn is None:
            return await inter.response.send_message(tag, ephemeral=True)
        await inter.response.send_modal(AddTagButtonModal(self, tag))

    @urls.command(name="edit", description="Edit a button for a tag.")
    @describe(name="The name of the tag you want to edit button from.")
    @autocomplete(name=tag_button_completer)
    async def button_edit(self, inter: Interaction, name: str):
        tag = await self.check_conn_tag(name)
        if isinstance(tag, str) or self._conn is None:
            return await inter.response.send_message(tag, ephemeral=True)
        try:
            button_sel = TagSelectButton(self, tag)
            button_view = View()
            button_view.add_item(button_sel)
            await inter.response.send_message(view=button_view, ephemeral=True)
        except:
            button_sel = TagSelectButton(self, tag, safe=True)
            button_view = View()
            button_view.add_item(button_sel)
            await inter.response.send_message(view=button_view, ephemeral=True)

    @urls.command(name="delete", description="Delete button(s) for a tag.")
    @describe(name="The name of the tag you want to delete button(s) from.")
    @autocomplete(name=tag_button_completer)
    async def button_delete(self, inter: Interaction, name: str):
        tag = await self.check_conn_tag(name)
        if isinstance(tag, str) or self._conn is None:
            return await inter.response.send_message(tag, ephemeral=True)
        button_sel = TagSelectButton(self, tag, True)
        button_view = View()
        button_view.add_item(button_sel)
        await inter.response.send_message(view=button_view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(await Tags.setup(bot))
