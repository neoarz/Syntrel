import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


def purge_command():
    @commands.hybrid_command(
        name="purge",
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(
        amount="The amount of messages that should be deleted.",
        user="The user whose messages should be deleted (optional).",
    )
    async def purge(self, context, amount: int, user: discord.Member = None):
        if context.interaction:
            await context.defer(ephemeral=True)

        if user:
            deleted_count = 0

            def check(message):
                nonlocal deleted_count
                if message.author == user and deleted_count < amount:
                    deleted_count += 1
                    return True
                return False

            purged_messages = await context.channel.purge(limit=300, check=check)
        else:
            purged_messages = await context.channel.purge(limit=amount)

        embed = discord.Embed(
            title="Purge",
            description=f"**{context.author}** cleared **{len(purged_messages)}** messages!"
            + (f" from **{user}**" if user else ""),
            color=0x7289DA,
        )
        embed.set_author(
            name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png"
        )

        if context.interaction:
            await context.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed, delete_after=10)

    return purge
