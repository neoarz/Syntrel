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

    @commands.hybrid_command(
        name="coinflip",
        description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context):
        return await coinflip_command()(self, context)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    async def eight_ball(self, context, *, question: str):
        return await eightball_command()(self, context, question=question)

    @commands.hybrid_command(
        name="minesweeper", 
        description="Play a buttoned minesweeper mini-game."
    )
    async def minesweeper(self, context):
        return await minesweeper_command()(self, context)

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context):
        return await randomfact_command()(self, context)

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
