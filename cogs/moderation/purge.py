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
    @app_commands.describe(amount="The amount of messages that should be deleted.")
    async def purge(self, context, amount: int):
        await context.send("Deleting messages...")
        purged_messages = await context.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title="Purge",
            description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages!",
            color=0x7289DA,
        )
        embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
        await context.channel.send(embed=embed)
    
    return purge
