import discord
from discord.ext import commands
from discord.ext.commands import Context

from .rickroll import rr_command
from .labubu import labubu_command
from .tryitandsee import tryitandsee_command
from .piracy import piracy_command
from .keanu import keanu_command

class Miscellaneous(commands.GroupCog, name="miscellaneous"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="miscellaneous", invoke_without_command=True)
    async def miscellaneous_group(self, context: Context):
        embed = discord.Embed(
            title="Miscellaneous Commands",
            description="Use `.miscellaneous <subcommand>` or `/miscellaneous <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="Miscellaneous", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.add_field(name="Available", value="rr, labubu, tryitandsee, piracy, keanu", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown miscellaneous command: {name}")

    @miscellaneous_group.command(name="rr")
    async def miscellaneous_group_rr(self, context: Context):
        await self._invoke_hybrid(context, "rr")

    @miscellaneous_group.command(name="labubu")
    async def miscellaneous_group_labubu(self, context: Context):
        await self._invoke_hybrid(context, "labubu")

    @miscellaneous_group.command(name="tryitandsee")
    async def miscellaneous_group_tryitandsee(self, context: Context):
        await self._invoke_hybrid(context, "tryitandsee")

    @miscellaneous_group.command(name="piracy")
    async def miscellaneous_group_piracy(self, context: Context):
        await self._invoke_hybrid(context, "piracy")

    @miscellaneous_group.command(name="keanu")
    async def miscellaneous_group_keanu(self, context: Context):
        await self._invoke_hybrid(context, "keanu")

    @commands.hybrid_command(
        name="rr",
        description="Rickroll"
    )
    async def rr(self, context):
        return await rr_command()(self, context)

    @commands.hybrid_command(
        name="labubu",
        description="Labubu ASCII art"
    )
    async def labubu(self, context):
        return await labubu_command()(self, context)

    @commands.hybrid_command(
        name="tryitandsee",
        description="Try it and see"
    )
    async def tryitandsee(self, context):
        return await tryitandsee_command()(self, context)

    @commands.hybrid_command(
        name="piracy",
        description="FBI Anti Piracy Warning"
    )
    async def piracy(self, context):
        return await piracy_command()(self, context)

    @commands.hybrid_command(
        name="keanu",
        description="Reeves"
    )
    async def keanu(self, context):
        return await keanu_command()(self, context)

async def setup(bot) -> None:
    cog = Miscellaneous(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'miscellaneous.rr'")
    bot.logger.info("Loaded extension 'miscellaneous.labubu'")
    bot.logger.info("Loaded extension 'miscellaneous.tryitandsee'")
    bot.logger.info("Loaded extension 'miscellaneous.piracy'")
    bot.logger.info("Loaded extension 'miscellaneous.keanu'")
