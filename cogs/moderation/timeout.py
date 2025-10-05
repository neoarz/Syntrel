import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta


def timeout_command():
    DURATION_CHOICES = [
        app_commands.Choice(name="60 secs", value="60s"),
        app_commands.Choice(name="5 mins", value="5m"),
        app_commands.Choice(name="10 mins", value="10m"),
        app_commands.Choice(name="1 hour", value="1h"),
        app_commands.Choice(name="1 day", value="1d"),
        app_commands.Choice(name="1 week", value="1w"),
    ]
    @commands.hybrid_command(
        name="timeout",
        description="Timeout a user for a specified duration.",
    )
    @app_commands.describe(
        user="The user that should be timed out.",
        duration="Duration",
        reason="The reason why the user should be timed out.",
    )
    @app_commands.choices(duration=DURATION_CHOICES)
    async def timeout(
        self, context, user: discord.User, duration: str, *, reason: str = "Not specified"
    ):
        try:
            member = context.guild.get_member(user.id)
            if not member:
                try:
                    member = await context.guild.fetch_member(user.id)
                except discord.NotFound:
                    embed = discord.Embed(
                        title="Error!",
                        description="This user is not in the server.",
                        color=0xE02B2B,
                    ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                    await context.send(embed=embed, ephemeral=True)
                    return

            if not context.author.guild_permissions.moderate_members and context.author != context.guild.owner:
                embed = discord.Embed(
                    title="Missing Permissions!",
                    description="You don't have the `Timeout Members` permission to use this command.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                await context.send(embed=embed, ephemeral=True)
                return

            if member and member.top_role >= context.guild.me.top_role:
                embed = discord.Embed(
                    title="Cannot Timeout User",
                    description="This user has a higher or equal role to me. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                await context.send(embed=embed, ephemeral=True)
                return

            if member and context.author != context.guild.owner:
                if member.top_role >= context.author.top_role:
                    embed = discord.Embed(
                        title="Cannot Timeout User",
                        description="You cannot timeout this user as they have a higher or equal role to you.",
                        color=0xE02B2B,
                    ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                    await context.send(embed=embed, ephemeral=True)
                    return

            seconds = _parse_duration_to_seconds(duration)
            if seconds is None or seconds <= 0:
                embed = discord.Embed(
                    title="Invalid Duration",
                    description="Choose one of: 60 secs, 5 mins, 10 mins, 1 hour, 1 day, 1 week.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                await context.send(embed=embed, ephemeral=True)
                return

            max_seconds = 28 * 24 * 60 * 60
            seconds = min(seconds, max_seconds)

            try:
                timeout_delta = timedelta(seconds=seconds)
                await member.timeout(timeout_delta, reason=reason)

                embed = discord.Embed(
                    title="Timeout",
                    description=f"**{user}** was timed out by **{context.author}**!",
                    color=0x7289DA,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                embed.add_field(name="Reason:", value=reason)
                embed.add_field(name="Duration:", value=_format_duration(duration), inline=False)
                await context.send(embed=embed)

            except discord.Forbidden:
                embed = discord.Embed(
                    title="Error!",
                    description="I don't have permission to timeout this user. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                await context.send(embed=embed, ephemeral=True)
            except discord.HTTPException as e:
                embed = discord.Embed(
                    title="Error!",
                    description=f"Discord API error: {str(e)}",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                await context.send(embed=embed, ephemeral=True)
            except Exception as e:
                embed = discord.Embed(
                    title="Debug Error!",
                    description=f"Error type: {type(e).__name__}\nError message: {str(e)}",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                await context.send(embed=embed, ephemeral=True)

        except Exception:
            embed = discord.Embed(
                title="Error!",
                description="An unexpected error occurred.",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
            await context.send(embed=embed, ephemeral=True)

    @timeout.autocomplete("duration")
    async def duration_autocomplete(interaction: discord.Interaction, current: str):
        query = (current or "").lower()
        filtered = [c for c in DURATION_CHOICES if query in c.name.lower() or query in c.value.lower()]
        return filtered[:25]

    return timeout


def _parse_duration_to_seconds(duration: str):
    try:
        s = duration.strip().lower()
        if s.endswith("s"):
            return int(s[:-1])
        if s.endswith("m"):
            return int(s[:-1]) * 60
        if s.endswith("h"):
            return int(s[:-1]) * 60 * 60
        if s.endswith("d"):
            return int(s[:-1]) * 60 * 60 * 24
        if s.endswith("w"):
            return int(s[:-1]) * 60 * 60 * 24 * 7
        return int(s)
    except Exception:
        return None


def _format_duration(duration: str) -> str:
    mapping = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
    }
    s = duration.strip().lower()
    for suffix, word in mapping.items():
        if s.endswith(suffix):
            try:
                value = int(s[:-1])
                return f"{value} {word}"
            except Exception:
                return duration
    try:
        value = int(s)
        return f"{value} seconds"
    except Exception:
        return duration


