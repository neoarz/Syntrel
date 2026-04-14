import discord
from discord import app_commands
from discord.ext import commands


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
        if not context.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You are missing the permission(s) `manage_messages` to execute this command!",
                color=0xE02B2B,
            ).set_author(
                name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png"
            )
            await context.send(embed=embed, ephemeral=True)
            return

        if not context.guild.me.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="I am missing the permission(s) `manage_messages` to execute this command!",
                color=0xE02B2B,
            ).set_author(
                name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png"
            )
            await context.send(embed=embed, ephemeral=True)
            return

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
