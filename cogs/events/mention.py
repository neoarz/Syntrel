import discord
import random
from discord.ext import commands


class MentionListener(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user or message.author.bot:
            return

        if self.bot.user in message.mentions:
            try:
                emoji_options = [
                    "<a:PandaPing:1417550314260926575>",
                    "<:PandaPing2:1434998389451395224>",
                    "<:PandaPing3:1434998524696723466>",
                ]
                selected_emoji = random.choice(emoji_options)
                self.bot.logger.debug(
                    f"Attempting to react with emoji: {selected_emoji}"
                )
                await message.add_reaction(selected_emoji)
                self.bot.logger.debug("Successfully reacted with mention emoji")
            except Exception as e:
                self.bot.logger.debug(f"Failed to react with mention emoji: {e}")
                try:
                    self.bot.logger.debug("Falling back to wave emoji")
                    await message.add_reaction("👋")
                    self.bot.logger.debug("Successfully reacted with wave emoji")
                except Exception as fallback_error:
                    self.bot.logger.debug(
                        f"Failed to react with fallback emoji: {fallback_error}"
                    )

        await self.bot.process_commands(message)


