import os
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Archive(commands.Cog, name="archive"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="archive",
        description="Archives in a text file the last messages with a chosen limit of messages.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        limit="The limit of messages that should be archived.",
    )
    async def archive(self, context: Context, limit: int = 10) -> None:
        """
        Archives in a text file the last messages with a chosen limit of messages. This command requires the MESSAGE_CONTENT intent to work properly.

        :param context: The hybrid command context.
        :param limit: The limit of messages that should be archived. Default is 10.
        """
        log_file = f"{context.channel.id}.log"
        
        messages = []
        async for message in context.channel.history(
            limit=limit, before=context.message
        ):
            attachments = []
            for attachment in message.attachments:
                attachments.append(attachment.url)
            attachments_text = (
                f"[Attached File{'s' if len(attachments) >= 2 else ''}: {', '.join(attachments)}]"
                if len(attachments) >= 1
                else ""
            )
            
            message_line = f"{message.created_at.strftime('%d.%m.%Y %H:%M:%S')} {message.author} {message.id}: {message.clean_content} {attachments_text}\n"
            messages.append(message_line)
        
        with open(log_file, "w", encoding="UTF-8") as f:
            f.write(
                f'Archived messages from: #{context.channel} ({context.channel.id}) in the guild "{context.guild}" ({context.guild.id}) at {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
            )

            for message_line in reversed(messages):
                f.write(message_line)
        
        f = discord.File(log_file)
        await context.send(file=f)
        os.remove(log_file)


async def setup(bot) -> None:
    await bot.add_cog(Archive(bot))