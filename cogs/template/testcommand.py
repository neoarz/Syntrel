"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.4.0
"""

from discord.ext import commands
from discord.ext.commands import Context


class TestCommand(commands.Cog, name="testcommand"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="testcommand",
        description="This is a testing command that does nothing.",
    )
    async def testcommand(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        pass


async def setup(bot) -> None:
    await bot.add_cog(TestCommand(bot))
