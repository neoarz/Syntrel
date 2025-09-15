import random
import discord
from discord.ext import commands
from discord.ext.commands import Context

class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.red)
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "tails"
        self.stop()

class CoinFlip(commands.Cog, name="coinflip"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.
        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(
            title="Coinflip",
            description="What is your bet?", 
            color=0x7289DA
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                title="Coinflip",
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0x00FF00,
            )
            embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        else:
            embed = discord.Embed(
                title="Coinflip",
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
            embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        await message.edit(embed=embed, view=None, content=None)

async def setup(bot) -> None:
    await bot.add_cog(CoinFlip(bot))