import discord
from discord.ext import commands
from discord.ext.commands import Context


class Shutdown(commands.Cog, name="shutdown"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()


async def setup(bot) -> None:
    await bot.add_cog(Shutdown(bot))
