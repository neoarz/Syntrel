import platform
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime
import pytz
from utils.contributors import generate_contributors_image


class FeedbackForm(discord.ui.Modal, title="Feedback"):
    feedback = discord.ui.TextInput(
        label="What do you think about this bot?",
        style=discord.TextStyle.long,
        placeholder="Type your answer here...",
        required=True,
        max_length=256,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Thank You!",
                description="Your feedback has been submitted, the owners have been notified about it.",
                color=0x7289DA,
            ).set_author(
                name="Feedback System",
                icon_url="https://yes.nighty.works/raw/gSxqzV.png",
            ),
            ephemeral=True,
        )

        app_owner = (await self.bot.application_info()).owner
        await app_owner.send(
            embed=discord.Embed(
                title="New Feedback",
                description=f"{interaction.user} (<@{interaction.user.id}>) has submitted a new feedback:\n```\n{self.feedback.value}\n```",
                color=0x7289DA,
            ).set_author(
                name="Feedback System",
                icon_url="https://yes.nighty.works/raw/gSxqzV.png",
            )
        )


class BotInfoView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

        github_emoji = discord.PartialEmoji(name="githubicon", id=1417717356846776340)
        github_button = discord.ui.Button(
            label="GitHub",
            emoji=github_emoji,
            url="https://github.com/neoarz/syntrel",
            style=discord.ButtonStyle.link,
        )
        self.add_item(github_button)

        feedback_emoji = discord.PartialEmoji(
            name="ThumbsUpBlueEmoji", id=1426066711500554302
        )
        feedback_button = discord.ui.Button(
            label="Feedback",
            emoji=feedback_emoji,
            style=discord.ButtonStyle.secondary,
            custom_id="feedback_button",
        )
        feedback_button.callback = self.feedback_callback
        self.add_item(feedback_button)

        bug_emoji = discord.PartialEmoji(name="BugHunterBadge", id=1425703361625460856)
        bug_button = discord.ui.Button(
            label="Bug Report",
            emoji=bug_emoji,
            url="https://github.com/neoarz/Syntrel/issues",
            style=discord.ButtonStyle.link,
        )
        self.add_item(bug_button)

    async def feedback_callback(self, interaction: discord.Interaction):
        feedback_form = FeedbackForm(self.bot)
        await interaction.response.send_modal(feedback_form)


class BotInfo(commands.Cog, name="botinfo"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = guild.system_channel or next(
            (
                c
                for c in guild.text_channels
                if c.permissions_for(guild.me).send_messages
            ),
            None,
        )

        if channel:
            ny_tz = pytz.timezone("America/New_York")
            current_time = datetime.now(ny_tz).strftime("%m/%d/%y, %I:%M %p")

            description_text = (
                'Heyooo! I\'m Syntrel, a bot made to help with [SideStore](https://discord.gg/3DwCwpBHfv), [MeloNX](https://discord.gg/Q4VkbkYfmk), and [idevice](https://discord.gg/ZnNcrRT3M8). I even have some cool extras! If you encounter any issues, please file a bug report. If you have any feedback or suggestions, simply select "Feedback"! <:HeardPanda:1417619745896660992>\n\n'
                "**New to Syntrel?** Run `/help` to get started and explore all available commands!\n\n"
                f"**Owner:** [neoarz](https://discordapp.com/users/1015372540937502851)\n"
                f"**Python Version:** {platform.python_version()}\n"
                f"**Discord.py Version:** {discord.__version__}\n"
                f"**Prefix:** / (Slash Commands) or {self.bot.bot_prefix} for normal commands"
            )

            embed = discord.Embed(
                title="Syntrel Discord Bot",
                description=description_text,
                color=0x7289DA,
            )
            embed.set_author(
                name="Syntrel",
                icon_url="https://github.com/neoarz/Syntrel/blob/main/assets/icon.png?raw=true",
            )
            embed.set_image(
                url="https://github.com/neoarz/Syntrel/raw/main/assets/bannerdark.png"
            )
            embed.set_footer(
                text=f"neoarz • {current_time}",
                icon_url="https://yes.nighty.works/raw/P1Us35.webp",
            )

            view = BotInfoView(self.bot)

            await channel.send(embed=embed, view=view)
        else:
            self.bot.logger.warning(f"Couldn't find a suitable channel in {guild.name}")

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def botinfo(self, context: Context) -> None:
        if context.interaction:
            await context.interaction.response.defer(ephemeral=False)

        ny_tz = pytz.timezone("America/New_York")
        current_time = datetime.now(ny_tz).strftime("%m/%d/%y, %I:%M %p")

        description_text = (
            'Heyooo! I\'m Syntrel, a bot made to help with [SideStore](https://discord.gg/3DwCwpBHfv), [MeloNX](https://discord.gg/Q4VkbkYfmk), and [idevice](https://discord.gg/ZnNcrRT3M8). I even have some cool extras! If you encounter any issues, please file a bug report. If you have any feedback or suggestions, simply select "Feedback"! <:HeardPanda:1417619745896660992>\n\n'
            "**New to Syntrel?** Run `/help` to get started and explore all available commands!\n\n"
            f"**Owner:** [neoarz](https://discordapp.com/users/1015372540937502851)\n"
            f"**Python Version:** {platform.python_version()}\n"
            f"**Discord.py Version:** {discord.__version__}\n"
            f"**Prefix:** / (Slash Commands) or {self.bot.bot_prefix} for normal commands"
        )

        embed1 = discord.Embed(
            title="Syntrel Discord Bot",
            description=description_text,
            color=0x7289DA,
        )
        embed1.set_author(
            name="Syntrel",
            icon_url="https://github.com/neoarz/Syntrel/blob/main/assets/icon.png?raw=true",
        )
        embed1.set_image(
            url="https://github.com/neoarz/Syntrel/raw/main/assets/bannerdark.png"
        )
        embed1.set_footer(
            text=f"neoarz • {current_time}",
            icon_url="https://yes.nighty.works/raw/P1Us35.webp",
        )

        embed2 = discord.Embed(
            title="Contributors",
            description="Giving credit where it's due! <a:pandasquish:1428617277317709915>",
            color=0x7289DA,
        )

        contributors_image = generate_contributors_image()

        view = BotInfoView(self.bot)

        if contributors_image:
            file = discord.File(contributors_image, filename="contributors.png")
            embed2.set_image(url="attachment://contributors.png")

            if context.interaction:
                await context.interaction.followup.send(
                    embeds=[embed1, embed2], file=file, view=view
                )
            else:
                await context.send(embeds=[embed1, embed2], file=file, view=view)
        else:
            if context.interaction:
                await context.interaction.followup.send(
                    embeds=[embed1, embed2], view=view
                )
            else:
                await context.send(embeds=[embed1, embed2], view=view)


async def setup(bot) -> None:
    await bot.add_cog(BotInfo(bot))
