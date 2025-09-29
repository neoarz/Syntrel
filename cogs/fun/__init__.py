import discord
from discord.ext import commands
from discord.ext.commands import Context

from .coinflip import coinflip_command
from .eightball import eightball_command
from .minesweeper import minesweeper_command
from .randomfact import randomfact_command
from .rockpaperscissors import rps_command

class Fun(commands.GroupCog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="fun", invoke_without_command=True)
    async def fun_group(self, context: Context):
        embed = discord.Embed(
            title="Fun Commands",
            description="Use `.fun <subcommand>` or slash `/fun <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        embed.add_field(name="Available", value="coinflip, 8ball, minesweeper, randomfact, rps", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, **kwargs):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command, **kwargs)
        else:
            await context.send(f"Unknown fun command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @fun_group.command(name="coinflip")
    async def fun_group_coinflip(self, context: Context):
        await self._invoke_hybrid(context, "coinflip")

    @fun_group.command(name="8ball")
    async def fun_group_8ball(self, context: Context, *, question: str):
        await self._invoke_hybrid(context, "8ball", question=question)

    @fun_group.command(name="minesweeper")
    async def fun_group_minesweeper(self, context: Context):
        await self._invoke_hybrid(context, "minesweeper")

    @fun_group.command(name="randomfact")
    async def fun_group_randomfact(self, context: Context):
        await self._invoke_hybrid(context, "randomfact")

    @fun_group.command(name="rps")
    async def fun_group_rps(self, context: Context):
        await self._invoke_hybrid(context, "rps")

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="coinflip",
        description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context):
        return await coinflip_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    async def eight_ball(self, context, *, question: str):
        return await eightball_command()(self, context, question=question)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="minesweeper", 
        description="Play a buttoned minesweeper mini-game."
    )
    async def minesweeper(self, context):
        return await minesweeper_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context):
        return await randomfact_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context):
        return await rps_command()(self, context)

async def setup(bot) -> None:
    cog = Fun(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'fun.coinflip'")
    bot.logger.info("Loaded extension 'fun.8ball'")
    bot.logger.info("Loaded extension 'fun.minesweeper'")
    bot.logger.info("Loaded extension 'fun.randomfact'")
    bot.logger.info("Loaded extension 'fun.rps'")
