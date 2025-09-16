import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Warnings(commands.Cog, name="warnings"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def send_embed(self, context: Context, embed: discord.Embed, *, ephemeral: bool = False) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await context.send(embed=embed)

    @commands.hybrid_group(
        name="warning",
        description="Manage warnings of a user on a server.",
    )
    async def warning(self, context: Context) -> None:
        """
        Manage warnings of a user on a server.

        :param context: The hybrid command context.
        """
        if not context.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You are missing the permission(s) `manage_messages` to execute this command!",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            return await self.send_embed(context, embed, ephemeral=True)
        
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="Warning",
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
                color=0x7289DA,
            )
            embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await self.send_embed(context, embed)

    @warning.command(
        name="add",
        description="Adds a warning to a user in the server.",
    )
    @app_commands.describe(
        user="The user that should be warned.",
        reason="The reason why the user should be warned.",
    )
    async def warning_add(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        if not context.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You are missing the permission(s) `manage_messages` to execute this command!",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            return await self.send_embed(context, embed, ephemeral=True)
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await self.bot.database.add_warn(
            user.id, context.guild.id, context.author.id, reason
        )
        embed = discord.Embed(
            title="Warning",
            description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
            color=0x7289DA,
        )
        embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        embed.add_field(name="Reason:", value=reason)
        await self.send_embed(context, embed)
        try:
            dm_embed = discord.Embed(
                title="Warning",
                description=f"You were warned by **{context.author}** in **{context.guild.name}**!\nReason: {reason}",
                color=0xE02B2B,
            )
            dm_embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await member.send(embed=dm_embed)
        except:
            fallback = discord.Embed(
                title="Warning",
                description=f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}",
                color=0xE02B2B,
            )
            await self.send_embed(context, fallback)

    @warning.command(
        name="remove",
        description="Removes a warning from a user in the server.",
    )
    @app_commands.describe(
        user="The user that should get their warning removed.",
        warn_id="The ID of the warning that should be removed.",
    )
    async def warning_remove(
        self, context: Context, user: discord.User, warn_id: int
    ) -> None:
        """
        Removes a warning from a user.

        :param context: The hybrid command context.
        :param user: The user that should get their warning removed.
        :param warn_id: The ID of the warning that should be removed.
        """
        if not context.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You are missing the permission(s) `manage_messages` to execute this command!",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            return await self.send_embed(context, embed, ephemeral=True)
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await self.bot.database.remove_warn(warn_id, user.id, context.guild.id)
        embed = discord.Embed(
            title="Warning",
            description=f"I've removed the warning **#{warn_id}** from **{member}**!\nTotal warns for this user: {total}",
            color=0x7289DA,
        )
        embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        await self.send_embed(context, embed)

    @warning.command(
        name="list",
        description="Shows the warnings of a user in the server.",
    )
    @app_commands.describe(user="The user you want to get the warnings of.")
    async def warning_list(self, context: Context, user: discord.User) -> None:
        """
        Shows the warnings of a user in the server.

        :param context: The hybrid command context.
        :param user: The user you want to get the warnings of.
        """
        if not context.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You are missing the permission(s) `manage_messages` to execute this command!",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            return await self.send_embed(context, embed, ephemeral=True)
        warnings_list = await self.bot.database.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(title=f"Warnings of {user}", color=0x7289DA)
        embed.set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        description = ""
        if len(warnings_list) == 0:
            description = "This user has no warnings."
        else:
            for warning in warnings_list:
                description += f"• Warned by <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>) - Warn ID #{warning[5]}\n"
        embed.description = description
        await self.send_embed(context, embed)



async def setup(bot) -> None:
    await bot.add_cog(Warnings(bot))
