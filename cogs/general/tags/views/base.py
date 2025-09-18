import logging
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(f"discord_bot.{self.__class__.__name__}")

    @classmethod
    async def setup(cls, bot):
        return cls(bot)

    async def cog_unload(self):
        pass
