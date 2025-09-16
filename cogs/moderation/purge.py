import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Purge(commands.Cog, name="purge"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="purge",
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(amount="The amount of messages that should be deleted.")
    async def purge(self, context: Context, amount: int) -> None:
        """
        Delete a number of messages.

        :param context: The hybrid command context.
        :param amount: The number of messages that should be deleted.
        """
        await context.send("Deleting messages...")
        purged_messages = await context.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title="Purge",
            description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages!",
            color=0x7289DA,
        )
        embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        await context.channel.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Purge(bot))
