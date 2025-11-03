import discord
from discord.ext import commands


def serverinfo_command():
    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @commands.guild_only()
    async def serverinfo(self, context):
        if context.guild is None:
            await context.send("This command can only be used in a server, not in DMs!")
            return

        guild = context.guild

        text_channels = len(
            [c for c in guild.channels if isinstance(c, discord.TextChannel)]
        )
        voice_channels = len(
            [c for c in guild.channels if isinstance(c, discord.VoiceChannel)]
        )
        category_channels = len(
            [c for c in guild.channels if isinstance(c, discord.CategoryChannel)]
        )
        forum_channels = len(
            [c for c in guild.channels if isinstance(c, discord.ForumChannel)]
        )
        stage_channels = len(
            [c for c in guild.channels if isinstance(c, discord.StageChannel)]
        )

        age_restricted = len(
            [c for c in guild.channels if hasattr(c, "nsfw") and c.nsfw]
        )
        hidden_channels = len(
            [
                c
                for c in guild.channels
                if c.permissions_for(guild.default_role).view_channel == False
            ]
        )

        managed_roles = len([r for r in guild.roles if r.managed])

        animated_emojis = len([e for e in guild.emojis if e.animated])
        managed_emojis = len([e for e in guild.emojis if e.managed])
        unavailable_emojis = len([e for e in guild.emojis if not e.available])

        png_stickers = len(
            [s for s in guild.stickers if s.format == discord.StickerFormatType.png]
        )
        apng_stickers = len(
            [s for s in guild.stickers if s.format == discord.StickerFormatType.apng]
        )
        gif_stickers = len(
            [s for s in guild.stickers if s.format == discord.StickerFormatType.lottie]
        )
        lottie_stickers = len(
            [s for s in guild.stickers if s.format == discord.StickerFormatType.lottie]
        )

        online_members = len(
            [m for m in guild.members if m.status == discord.Status.online]
        )
        idle_members = len(
            [m for m in guild.members if m.status == discord.Status.idle]
        )
        dnd_members = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline_members = len(
            [m for m in guild.members if m.status == discord.Status.offline]
        )

        bot_count = len([m for m in guild.members if m.bot])
        human_count = guild.member_count - bot_count

        created_delta = discord.utils.utcnow() - guild.created_at
        years_ago = created_delta.days // 365

        embed = discord.Embed(
            title=f"**Server Name:** {guild.name}", color=0x7289DA
        ).set_author(
            name="Server Information",
            icon_url="https://yes.nighty.works/raw/gSxqzV.png",
        )

        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)

        owner_value = (
            guild.owner.mention
            if guild.owner
            else (f"<@{guild.owner_id}>" if guild.owner_id else "Unknown")
        )
        embed.add_field(name="Owner", value=owner_value, inline=True)

        embed.add_field(
            name="Created",
            value=f"{years_ago} year{'s' if years_ago != 1 else ''} ago",
            inline=True,
        )

        embed.add_field(
            name="Max Members",
            value=f"{guild.max_members:,}" if guild.max_members else "Unknown",
            inline=True,
        )

        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count or 0
        embed.add_field(
            name="Boost Status",
            value=f"Level {boost_level}, {boost_count} Boost{'s' if boost_count != 1 else ''}",
            inline=False,
        )

        channels_info = f"{text_channels} text, {voice_channels} voice, {category_channels} category"
        if forum_channels > 0:
            channels_info += f", {forum_channels} forum"
        if stage_channels > 0:
            channels_info += f", {stage_channels} stage"
        channels_info += f"\n{age_restricted} age restricted, {hidden_channels} hidden"

        embed.add_field(
            name=f"Channels ({len(guild.channels)})", value=channels_info, inline=True
        )

        roles_info = f"{len(guild.roles)} total\n{managed_roles} managed"
        embed.add_field(
            name=f"Roles ({len(guild.roles)})", value=roles_info, inline=True
        )

        emotes_info = f"{len(guild.emojis)} total\n{animated_emojis} animated, {managed_emojis} managed"
        if unavailable_emojis > 0:
            emotes_info += f"\n{unavailable_emojis} unavailable"
        embed.add_field(
            name=f"Emotes ({len(guild.emojis)})", value=emotes_info, inline=True
        )

        if len(guild.stickers) > 0:
            stickers_info = f"{len(guild.stickers)} total\n{png_stickers} PNG, {apng_stickers} APNG, {gif_stickers} GIF, {lottie_stickers} Lottie"
            embed.add_field(
                name=f"Stickers ({len(guild.stickers)})",
                value=stickers_info,
                inline=True,
            )

        embed.add_field(
            name="Member Count", value=f"{guild.member_count}", inline=False
        )

        embed.set_footer(
            text=f"Server ID: {guild.id} • Created: {guild.created_at.strftime('%m/%d/%Y')}"
        )

        if getattr(context, "interaction", None):
            await context.interaction.response.send_message(
                embed=embed, ephemeral=False
            )
        else:
            await context.send(embed=embed)

    return serverinfo
