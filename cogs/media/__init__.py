import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import Optional

from .mcquote import mcquote_command
from .img2gif import img2gif_command
from .tweety import tweety_command
from .tts import tts_command


def _require_group_prefix(context: Context) -> bool:
    if getattr(context, "interaction", None):
        return True
    group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
    if not group:
        return True
    prefix = context.prefix or ""
    content = context.message.content.strip().lower()
    return content.startswith(f"{prefix}{group} ")


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Media(commands.GroupCog, name="media"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for bot mentions with 'tweety' command while replying to a message"""
        if message.author.bot:
            return

        if (
            self.bot.user in message.mentions
            and message.reference
            and message.reference.message_id
        ):
            content = message.content.lower()
            content_without_mention = (
                content.replace(f"<@{self.bot.user.id}>", "")
                .replace(f"<@!{self.bot.user.id}>", "")
                .strip()
            )

            if content_without_mention.strip() == "tweety":
                ctx = await self.bot.get_context(message)
                await self.tweety(ctx)

    @commands.group(name="media", invoke_without_command=True)
    async def media_group(self, context: Context):
        embed = discord.Embed(
            title="Media Commands",
            description="Use `.media <subcommand>` or `/media <subcommand>`.",
            color=0x7289DA,
        )
        embed.set_author(
            name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"
        )
        embed.add_field(
            name="Available",
            value="mcquote, img2gif, tweety, tts",
            inline=False,
        )
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, *args, **kwargs):
        if name == "mcquote":
            await self.mcquote(context, text=kwargs.get("text", ""))
            return
        if name == "img2gif":
            await self.img2gif(context, attachment=kwargs.get("attachment"))
            return
        if name == "tweety":
            await self.tweety(context)
            return
        if name == "tts":
            await self.tts(context, text=kwargs.get("text"))
            return
        await context.send(f"Unknown media command: {name}")

    @media_group.command(name="mcquote")
    async def media_group_mcquote(self, context: Context, *, text: str):
        await self._invoke_hybrid(context, "mcquote", text=text)

    @media_group.command(name="img2gif")
    async def media_group_img2gif(
        self, context: Context, attachment: Optional[discord.Attachment] = None
    ):
        await self._invoke_hybrid(context, "img2gif", attachment=attachment)

    @media_group.command(name="tweety")
    async def media_group_tweety(self, context: Context):
        await self._invoke_hybrid(context, "tweety")

    @media_group.command(name="tts")
    async def media_group_tts(self, context: Context, *, text: str = None):
        await self._invoke_hybrid(context, "tts", text=text)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="mcquote",
        description="Generate a custom Minecraft quote image.",
    )
    async def mcquote(self, context, *, text: str):
        return await mcquote_command()(self, context, text=text)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="img2gif",
        description="Convert an uploaded image to a GIF.",
    )
    async def img2gif(self, context, attachment: Optional[discord.Attachment] = None):
        return await img2gif_command()(self, context, attachment=attachment)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="tweety",
        description="Convert a replied message to a tweet image.",
    )
    async def tweety(self, context):
        return await tweety_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="tts",
        description="Convert text to speech using Google Text-to-Speech.",
    )
    async def tts(self, context, text: str = None):
        return await tts_command()(context, text=text)


async def setup(bot) -> None:
    cog = Media(bot)
    await bot.add_cog(cog)

    bot.logger.info("Loaded extension 'media.mcquote'")
    bot.logger.info("Loaded extension 'media.img2gif'")
    bot.logger.info("Loaded extension 'media.tweety'")
    bot.logger.info("Loaded extension 'media.tts'")
