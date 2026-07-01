import discord


def softban_command():
    async def softban(
        self,
        context,
        user: discord.User,
        *,
        reason: str = "Not specified",
        delete_messages: str = "none",
    ):
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
                description="I am missing the `Ban Members` permission to execute this command!",
                color=0xE02B2B,
            ).set_author(
                name="Moderation",
                icon_url="https://yes.nighty.works/raw/CPKHQd.png",
            )
            await context.send(embed=embed, ephemeral=True)
            return

        member = context.guild.get_member(user.id)
        if member is None:
            try:
                member = await context.guild.fetch_member(user.id)
            except discord.NotFound:
                member = None

        if member is not None:
            if member.top_role >= context.guild.me.top_role:
                embed = discord.Embed(
                    title="Cannot Softban User",
                    description="This user has a higher or equal role to me. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
                return

            if (
                context.author != context.guild.owner
                and member.top_role >= context.author.top_role
            ):
                embed = discord.Embed(
                    title="Cannot Softban User",
                    description="You cannot softban this user as they have a higher or equal role to you.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
                return

        delete_message_seconds = 0
        if delete_messages.endswith("h"):
            delete_message_seconds = min(int(delete_messages[:-1]) * 3600, 604800)
        elif delete_messages.endswith("d"):
            delete_message_seconds = min(int(delete_messages[:-1]) * 86400, 604800)

        try:
            if member is not None:
                try:
                    dm_embed = discord.Embed(
                        title="Softban",
                        description=f"You were softbanned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}",
                        color=0xE02B2B,
                    ).set_author(
                        name="Moderation",
                        icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                    )
                    await member.send(embed=dm_embed)
                except (discord.Forbidden, discord.HTTPException):
                    pass

            await context.guild.ban(
                user, reason=reason, delete_message_seconds=delete_message_seconds
            )
            await context.guild.unban(user, reason=f"Softban by {context.author}")

            embed = discord.Embed(
                title="Softban",
                description=f"**{user}** was softbanned by **{context.author}**!",
                color=0x7289DA,
            ).set_author(
                name="Moderation",
                icon_url="https://yes.nighty.works/raw/CPKHQd.png",
            )
            embed.add_field(name="Reason:", value=reason)
            await context.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="Error!",
                description="I don't have permission to softban this user. Make sure my role is above theirs.",
                color=0xE02B2B,
            ).set_author(
                name="Moderation",
                icon_url="https://yes.nighty.works/raw/CPKHQd.png",
            )
            await context.send(embed=embed, ephemeral=True)
        except discord.HTTPException as e:
            if "Cannot ban the owner of a guild" in str(e):
                embed = discord.Embed(
                    title="Cannot Softban User",
                    description="You cannot softban the server owner.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
            else:
                embed = discord.Embed(
                    title="Error!",
                    description=f"Discord API error: {str(e)}",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
            await context.send(embed=embed, ephemeral=True)

    return softban
