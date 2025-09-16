"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.4.0
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Ping(commands.Cog, name="ping"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x7289DA,
        )
        embed.set_author(name="Ping", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        if getattr(context, "interaction", None):
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Ping(bot))
