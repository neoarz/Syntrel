import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from .dontasktoask import dontasktoask_command
from .rickroll import rr_command
from .depart import depart_command
from .labubu import labubu_command
from .duck import duck_command
from .tryitandsee import tryitandsee_command
from .piracy import piracy_command
from .keanu import keanu_command
from .support import support_command
from .docs import docs_command
from .sigma import sigma_command
from .silly import silly_command
from .color import color_command


@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
class Miscellaneous(commands.GroupCog, name="misc"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name="miscellaneous", aliases=["misc"], invoke_without_command=True)
    async def miscellaneous_group(self, context: Context):
        embed = discord.Embed(
            title="Miscellaneous Commands",
            description="Use `.misc <subcommand>` or `/misc <subcommand>`.",
            color=0x7289DA
        )
        embed.set_author(name="Miscellaneous", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        embed.add_field(name="Available", value="dontasktoask, rr, depart, labubu, duck, tryitandsee, piracy, keanu, support, docs, sigma, silly, color", inline=False)
        await context.send(embed=embed)

    async def _invoke_hybrid(self, context: Context, name: str):
        command = self.bot.get_command(name)
        if command is not None:
            await context.invoke(command)
        else:
            await context.send(f"Unknown miscellaneous command: {name}")

    def _require_group_prefix(context: Context) -> bool:
        if getattr(context, "interaction", None):
            return True
        group = getattr(getattr(context, "cog", None), "qualified_name", "").lower()
        if not group:
            return True
        prefix = context.prefix or ""
        content = context.message.content.strip().lower()
        return content.startswith(f"{prefix}{group} ")

    @miscellaneous_group.command(name="dontasktoask")
    async def miscellaneous_group_dontasktoask(self, context: Context):
        await self._invoke_hybrid(context, "dontasktoask")

    @miscellaneous_group.command(name="rr")
    async def miscellaneous_group_rr(self, context: Context):
        await self._invoke_hybrid(context, "rr")

    @miscellaneous_group.command(name="depart")
    async def miscellaneous_group_depart(self, context: Context):
        await self._invoke_hybrid(context, "depart")

    @miscellaneous_group.command(name="labubu")
    async def miscellaneous_group_labubu(self, context: Context):
        await self._invoke_hybrid(context, "labubu")

    @miscellaneous_group.command(name="duck")
    async def miscellaneous_group_duck(self, context: Context):
        await self._invoke_hybrid(context, "duck")

    @miscellaneous_group.command(name="tryitandsee")
    async def miscellaneous_group_tryitandsee(self, context: Context):
        await self._invoke_hybrid(context, "tryitandsee")

    @miscellaneous_group.command(name="piracy")
    async def miscellaneous_group_piracy(self, context: Context):
        await self._invoke_hybrid(context, "piracy")

    @miscellaneous_group.command(name="keanu")
    async def miscellaneous_group_keanu(self, context: Context):
        await self._invoke_hybrid(context, "keanu")

    @miscellaneous_group.command(name="support")
    async def miscellaneous_group_support(self, context: Context):
        await self._invoke_hybrid(context, "support")

    @miscellaneous_group.command(name="docs")
    async def miscellaneous_group_docs(self, context: Context):
        await self._invoke_hybrid(context, "docs")

    @miscellaneous_group.command(name="sigma")
    async def miscellaneous_group_sigma(self, context: Context):
        await self._invoke_hybrid(context, "sigma")

    @miscellaneous_group.command(name="silly")
    async def miscellaneous_group_silly(self, context: Context, message_type: str = "regular"):
        await self._invoke_hybrid(context, "silly", message_type=message_type)

    @miscellaneous_group.command(name="color")
    async def miscellaneous_group_color(self, context: Context):
        await self._invoke_hybrid(context, "color")

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="dontasktoask",
        description="Shows the 'Don't Ask to Ask' image."
    )
    async def dontasktoask(self, context):
        return await dontasktoask_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="rr",
        description="Rickroll"
    )
    async def rr(self, context):
        return await rr_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="depart",
        description="Show the departure meme"
    )
    async def depart(self, context):
        return await depart_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="labubu",
        description="Labubu ASCII art"
    )
    async def labubu(self, context):
        return await labubu_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="duck",
        description="Duck ASCII art"
    )
    async def duck(self, context):
        return await duck_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="tryitandsee",
        description="Try it and see"
    )
    async def tryitandsee(self, context):
        return await tryitandsee_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="piracy",
        description="FBI Anti Piracy Warning"
    )
    async def piracy(self, context):
        return await piracy_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="keanu",
        description="Reeves"
    )
    async def keanu(self, context):
        return await keanu_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="support",
        description="Support?"
    )
    async def support(self, context):
        return await support_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="docs",
        description="Shows the docs image."
    )
    async def docs(self, context):
        return await docs_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="sigma",
        description="i feel so sigma!"
    )
    async def sigma(self, context):
        return await sigma_command()(self, context)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="silly",
        description="Sends a silly message :3"
    )
    @app_commands.describe(
        message_type="Type of message to send (regular or animated)"
    )
    @app_commands.choices(message_type=[
        app_commands.Choice(name="Regular", value="regular"),
        app_commands.Choice(name="Animated", value="animated")
    ])
    async def silly(self, context, message_type: str = "regular"):
        return await silly_command()(self, context, message_type=message_type)

    @commands.check(_require_group_prefix)
    @commands.hybrid_command(
        name="color",
        description="Get a random color."
    )
    async def color(self, context):
        return await color_command()(self, context)

async def setup(bot) -> None:
    cog = Miscellaneous(bot)
    await bot.add_cog(cog)
    
    bot.logger.info("Loaded extension 'miscellaneous.dontasktoask'")
    bot.logger.info("Loaded extension 'miscellaneous.rr'")
    bot.logger.info("Loaded extension 'miscellaneous.depart'")
    bot.logger.info("Loaded extension 'miscellaneous.labubu'")
    bot.logger.info("Loaded extension 'miscellaneous.duck'")
    bot.logger.info("Loaded extension 'miscellaneous.tryitandsee'")
    bot.logger.info("Loaded extension 'miscellaneous.piracy'")
    bot.logger.info("Loaded extension 'miscellaneous.keanu'")
    bot.logger.info("Loaded extension 'miscellaneous.support'")
    bot.logger.info("Loaded extension 'miscellaneous.docs'")
    bot.logger.info("Loaded extension 'miscellaneous.sigma'")
    bot.logger.info("Loaded extension 'miscellaneous.silly'")
    bot.logger.info("Loaded extension 'miscellaneous.color'")