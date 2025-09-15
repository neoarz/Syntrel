import random
import discord
from discord.ext import commands
from discord.ext.commands import Context

class RockPaperScissors(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]
        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(title="Rock Paper Scissors", color=0xBEBEFE)
        result_embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")

        winner = (3 + user_choice_index - bot_choice_index) % 3
        
        # Get the user mention
        user_mention = interaction.user.mention
        
        if winner == 0:
            result_embed.description = f"**That's a draw!** You've chosen {user_choice} and I've chosen {bot_choice}.\n-# gg {user_mention}"
            result_embed.colour = 0xF59E42
        elif winner == 1:
            result_embed.description = f"**You won!** You've chosen {user_choice} and I've chosen {bot_choice}.\n-# gg {user_mention}"
            result_embed.colour = 0x57F287
        else:
            result_embed.description = f"**You lost!** You've chosen {user_choice} and I've chosen {bot_choice}.\n-# gg {user_mention}"
            result_embed.colour = 0xE02B2B

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )

class RockPaperScissorsView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(RockPaperScissors())

class RPS(commands.Cog, name="rps"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        view = RockPaperScissorsView()
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description="Please make your choice",
            color=0x7289DA
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        await context.send(embed=embed, view=view)

async def setup(bot) -> None:
    await bot.add_cog(RPS(bot))