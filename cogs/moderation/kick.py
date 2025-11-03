import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


def kick_command():
    @commands.hybrid_command(
        name="kick",
        description="Kicks a user from the server.",
    )
    @app_commands.describe(
        user="The user that should be kicked.",
        reason="The reason why the user should be kicked.",
    )
    async def kick(self, context, user: discord.User, *, reason: str = "Not specified"):
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
                    ).set_author(
                        name="Moderation",
                        icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                    )
                    await context.send(embed=embed, ephemeral=True)
                    return

            if (
                not context.author.guild_permissions.kick_members
                and context.author != context.guild.owner
            ):
                embed = discord.Embed(
                    title="Missing Permissions!",
                    description="You don't have the `Kick Members` permission to use this command.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
                return

            if member and member.top_role >= context.guild.me.top_role:
                embed = discord.Embed(
                    title="Cannot Kick User",
                    description="This user has a higher or equal role to me. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
                return

            if member and context.author != context.guild.owner:
                if member.top_role >= context.author.top_role:
                    embed = discord.Embed(
                        title="Cannot Kick User",
                        description="You cannot kick this user as they have a higher or equal role to you.",
                        color=0xE02B2B,
                    ).set_author(
                        name="Moderation",
                        icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                    )
                    await context.send(embed=embed, ephemeral=True)
                    return

            try:
                if member:
                    try:
                        await member.send(
                            embed=discord.Embed(
                                title="Kick",
                                description=f"You were kicked by **{context.author}** from **{context.guild.name}**!\nReason: {reason}",
                                color=0xE02B2B,
                            ).set_author(
                                name="Moderation",
                                icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                            )
                        )
                    except (discord.Forbidden, discord.HTTPException):
                        pass

                await member.kick(reason=reason)

                embed = discord.Embed(
                    title="Kick",
                    description=f"**{user}** was kicked by **{context.author}**!",
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
                    description="I don't have permission to kick this user. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)
            except discord.HTTPException as e:
                if "Cannot kick the owner of a guild" in str(e):
                    embed = discord.Embed(
                        title="Cannot Kick User",
                        description="You cannot kick the server owner.",
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
            except Exception as e:
                embed = discord.Embed(
                    title="Debug Error!",
                    description=f"Error type: {type(e).__name__}\nError message: {str(e)}",
                    color=0xE02B2B,
                ).set_author(
                    name="Moderation",
                    icon_url="https://yes.nighty.works/raw/CPKHQd.png",
                )
                await context.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description="An unexpected error occurred.",
                color=0xE02B2B,
            ).set_author(
                name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png"
            )
            await context.send(embed=embed, ephemeral=True)

    return kick
