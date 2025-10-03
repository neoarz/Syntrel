import discord
from discord.ext import commands
from discord.ext.commands import Context

from .download import download_command


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

    @commands.group(name="media", invoke_without_command=True)
    async def media_group(self, context: Context):
        embed = discord.Embed(
            title="Media Commands",
            description="Use `.media <subcommand>` or `/media <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        embed.add_field(name="Available", value="download", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown media command: {name}")

    @media_group.command(name="download")
    async def media_group_download(self, context: Context, *, url: str):
        await self._invoke_hybrid(context, "download", url=url)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="download",
        description="Download a video from a URL using yt-dlp.",
    )
    async def download(self, context, *, url: str):
        return await download_command()(self, context, url=url)

async def setup(bot) -> None:
    cog = Media(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'media.download'")
