from discord import Interaction

from .views.base import BaseCog
from .views.tags import CreateTagModal


class TagCreate:
    def __init__(self, cog: BaseCog):
        self.cog = cog

    async def create(self, inter: Interaction):
        """Create a new tag."""
        if self.cog._conn is None:
            await inter.response.send_message(f"Error: DB connection was None!", ephemeral=True)
            return
        await inter.response.send_modal(CreateTagModal(self.cog))
