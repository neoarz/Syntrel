import discord
from discord import app_commands
from discord.ext import commands


class FeedbackForm(discord.ui.Modal, title="Feeedback"):
    feedback = discord.ui.TextInput(
        label="What do you think about this bot?",
        style=discord.TextStyle.long,
        placeholder="Type your answer here...",
        required=True,
        max_length=256,
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.answer = str(self.feedback)
        self.stop()


class Feedback(commands.Cog, name="feedback"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="feedback", description="Submit a feedback for the owners of the bot"
    )
    async def feedback(self, interaction: discord.Interaction) -> None:
        """
        Submit a feedback for the owners of the bot.

        :param interaction: The application command interaction.
        """
        feedback_form = FeedbackForm()
        await interaction.response.send_modal(feedback_form)

        await feedback_form.wait()
        interaction = feedback_form.interaction
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Thank You!",
                description="Your feedback has been submitted, the owners have been notified about it.",
                color=0x7289DA,
            ).set_author(name="Feedback System", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        )

        app_owner = (await self.bot.application_info()).owner
        await app_owner.send(
            embed=discord.Embed(
                title="New Feedback",
                description=f"{interaction.user} (<@{interaction.user.id}>) has submitted a new feedback:\n```\n{feedback_form.answer}\n```",
                color=0x7289DA,
            ).set_author(name="Feedback System", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        )


async def setup(bot) -> None:
    await bot.add_cog(Feedback(bot))