import discord
from discord import app_commands
from discord.ext import commands


def hackban_command():
    @commands.hybrid_command(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        user_id="The user ID that should be banned.",
        reason="The reason why the user should be banned.",
    )
    async def hackban(self, context, user_id: str, *, reason: str = "Not specified"):
        """
        Bans a user without the user having to be in the server.

        :param context: The hybrid command context.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            if (
                not context.author.guild_permissions.ban_members
                and context.author != context.guild.owner
            ):
                embed = discord.Embed(
                    title="Missing Permissions!",
                    description="You don't have the `Ban Members` permission to use this command.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
                return

            if not context.guild.me.guild_permissions.ban_members:
                embed = discord.Embed(
                    title="Missing Permissions!",
                    description="I am missing the permission(s) `ban_members` to execute this command!",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
                return

            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(
                int(user_id)
            )
            embed = discord.Embed(
                title="Ban",
                description=f"**{user}** (ID: {user_id}) was banned by **{context.author}**!",
                color=0x7289DA,
            ).set_author(
                name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png"
            )
            embed.add_field(name="Reason:", value=reason)
            await context.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B,
            ).set_author(
                name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png"
            )
            await context.send(embed=embed)

    return hackban
