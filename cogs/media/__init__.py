import discord
from discord.ext import commands
from discord.ext.commands import Context
from typing import Optional

from .download import download_command
from .mcquote import mcquote_command
from .img2gif import img2gif_command
from .tweety import tweety_command


def _require_group_prefix(context: Context) -> bool:
    if getattr(context, "interaction", None):
        return True
    group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
    if not group:
        return True
    prefix = context.prefix or ""
    content = context.message.content.strip().lower()
    return content.startswith(f"{prefix}{group} ")

class Media(commands.GroupCog, name="media"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for bot mentions with 'tweety' command while replying to a message"""
        if message.author.bot:
            return
        
        if self.bot.user in message.mentions and message.reference and message.reference.message_id:
            content = message.content.lower()
            content_without_mention = content.replace(f'<@{self.bot.user.id}>', '').replace(f'<@!{self.bot.user.id}>', '').strip()
            
            if 'tweety' in content_without_mention:
                parts = content_without_mention.split()
                verified = "false"
                theme = "light"
                
                for i, part in enumerate(parts):
                    if part == 'tweety':
                        if i + 1 < len(parts):
                            if parts[i + 1] in ['verified', 'true', 'yes']:
                                verified = "true"
                        if 'dark' in parts or 'night' in parts:
                            theme = "dark"
                        break
                
                ctx = await self.bot.get_context(message)
                
                await self.tweety(ctx, verified=verified, theme=theme)

    @commands.group(name="media", invoke_without_command=True)
    async def media_group(self, context: Context):
        embed = discord.Embed(
            title="Media Commands",
            description="Use `.media <subcommand>` or `/media <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        embed.add_field(name="Available", value="download, mcquote, img2gif, tweety", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str, *args, **kwargs):
        if name == "download":
            await self.download(context, url=kwargs.get('url', ''))
            return
        if name == "mcquote":
            await self.mcquote(context, text=kwargs.get('text', ''))
            return
        if name == "img2gif":
            await self.img2gif(context, attachment=kwargs.get('attachment'))
            return
        if name == "tweety":
            await self.tweety(context, verified=kwargs.get('verified', "false"), theme=kwargs.get('theme', "light"))
            return
        await context.send(f"Unknown media command: {name}")

    @media_group.command(name="download")
    async def media_group_download(self, context: Context, *, url: str):
        await self._invoke_hybrid(context, "download", url=url)

    @media_group.command(name="mcquote")
    async def media_group_mcquote(self, context: Context, *, text: str):
        await self._invoke_hybrid(context, "mcquote", text=text)

    @media_group.command(name="img2gif")
    async def media_group_img2gif(self, context: Context, attachment: Optional[discord.Attachment] = None):
        await self._invoke_hybrid(context, "img2gif", attachment=attachment)

    @media_group.command(name="tweety")
    async def media_group_tweety(self, context: Context, verified: str = "false", theme: str = "light"):
        await self._invoke_hybrid(context, "tweety", verified=verified, theme=theme)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="download",
        description="Download a video from a URL using yt-dlp.",
    )
    async def download(self, context, *, url: str):
        return await download_command()(self, context, url=url)

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
    async def tweety(self, context, verified: str = "false", theme: str = "light"):
        return await tweety_command()(self, context, verified=verified, theme=theme)

async def setup(bot) -> None:
    cog = Media(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'media.download'")
    bot.logger.info("Loaded extension 'media.mcquote'")
    bot.logger.info("Loaded extension 'media.img2gif'")
    bot.logger.info("Loaded extension 'media.tweety'")
