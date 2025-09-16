import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Nick(commands.Cog, name="nick"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @app_commands.describe(
        user="The user that should have a new nickname.",
        nickname="The new nickname that should be set.",
    )
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ) -> None:
        """
        Change the nickname of a user on a server.

        :param context: The hybrid command context.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        if not context.author.guild_permissions.manage_nicknames:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You are missing the permission(s) `manage_nicknames` to execute this command!",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            return await context.send(embed=embed, ephemeral=True)
        
        if not context.guild.me.guild_permissions.manage_nicknames:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="I am missing the permission(s) `manage_nicknames` to execute this command!",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            return await context.send(embed=embed, ephemeral=True)

        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Nickname",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x7289DA,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")    
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")    
            await context.send(embed=embed, ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Nick(bot))
