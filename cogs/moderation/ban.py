import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


def ban_command():
    @commands.hybrid_command(
        name="ban",
        description="Bans a user from the server.",
    )
    @app_commands.describe(
        user="The user that should be banned.",
        reason="The reason why the user should be banned.",
        delete_messages="Delete messages from the user (choose time period).",
    )
    @app_commands.choices(delete_messages=[
        app_commands.Choice(name="Don't delete any messages", value="none"),
        app_commands.Choice(name="Last 1 hour", value="1h"),
        app_commands.Choice(name="Last 6 hours", value="6h"),
        app_commands.Choice(name="Last 12 hours", value="12h"),
        app_commands.Choice(name="Last 24 hours", value="1d"),
        app_commands.Choice(name="Last 3 days", value="3d"),
        app_commands.Choice(name="Last 7 days", value="7d"),
    ])
    async def ban(
        self, context, user: discord.User, *, reason: str = "Not specified", delete_messages: str = "none"
    ):
        try:
            member = context.guild.get_member(user.id)
            if not member:
                try:
                    member = await context.guild.fetch_member(user.id)
                except discord.NotFound:
                    try:
                        await context.guild.ban(user, reason=reason)
                        embed = discord.Embed(
                            title="Ban",
                            description=f"**{user}** was banned by **{context.author}**!",
                            color=0x7289DA,
                        ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                        embed.add_field(name="Reason:", value=reason)
                        await context.send(embed=embed)
                        return
                    except discord.Forbidden:
                        embed = discord.Embed(
                            title="Error!",
                            description="I don't have permission to ban this user.",
                            color=0xE02B2B,
                        ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                        await context.send(embed=embed, ephemeral=True)
                        return
                    except Exception:
                        embed = discord.Embed(
                            title="Error!",
                            description="An error occurred while trying to ban the user.",
                            color=0xE02B2B,
                        ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                        await context.send(embed=embed, ephemeral=True)
                        return
            
            if not context.author.guild_permissions.ban_members and context.author != context.guild.owner:
                embed = discord.Embed(
                    title="Missing Permissions!",
                    description="You don't have the `Ban Members` permission to use this command.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                await context.send(embed=embed, ephemeral=True)
                return
            
            if member and member.top_role >= context.guild.me.top_role:
                embed = discord.Embed(
                    title="Cannot Ban User",
                    description="This user has a higher or equal role to me. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                await context.send(embed=embed, ephemeral=True)
                return
            
            if member and context.author != context.guild.owner:
                if member.top_role >= context.author.top_role:
                    embed = discord.Embed(
                        title="Cannot Ban User", 
                        description="You cannot ban this user as they have a higher or equal role to you.",
                        color=0xE02B2B,
                    ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                    await context.send(embed=embed, ephemeral=True)
                    return
            
            delete_message_days = 0
            delete_all_messages = False
            
            if delete_messages != "none":
                if delete_messages == "all":
                    delete_all_messages = True
                    delete_message_days = 7
                elif delete_messages.endswith("h"):
                    hours = int(delete_messages[:-1])
                    delete_message_days = min(hours / 24, 7)
                elif delete_messages.endswith("d"):
                    days = int(delete_messages[:-1])
                    delete_message_days = min(days, 7)
            
            try:
                if member:
                    try:
                        dm_embed = discord.Embed(
                            title="Ban",
                            description=f"You were banned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}",
                            color=0xE02B2B,
                        ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")
                        await member.send(embed=dm_embed)
                    except (discord.Forbidden, discord.HTTPException):
                        pass
                
                if member:
                    await member.ban(reason=reason, delete_message_days=delete_message_days)
                else:
                    await context.guild.ban(user, reason=reason, delete_message_days=delete_message_days)
                
                if delete_all_messages:
                    await self.delete_all_user_messages(context.guild, user.id)
                
                embed = discord.Embed(
                    title="Ban",
                    description=f"**{user}** was banned by **{context.author}**!",
                    color=0x7289DA,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                embed.add_field(name="Reason:", value=reason)
                
                if delete_messages != "none":
                    if delete_all_messages:
                        embed.add_field(name="Messages Deleted:", value="All messages", inline=False)
                    else:
                        delete_time_text = self.format_delete_time(delete_messages)
                        embed.add_field(name="Messages Deleted:", value=delete_time_text, inline=False)
                
                await context.send(embed=embed)
                
            except discord.Forbidden:
                embed = discord.Embed(
                    title="Error!",
                    description="I don't have permission to ban this user. Make sure my role is above theirs.",
                    color=0xE02B2B,
                ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                await context.send(embed=embed, ephemeral=True)
            except discord.HTTPException as e:
                if "Cannot ban the owner of a guild" in str(e):
                    embed = discord.Embed(
                        title="Cannot Ban User",
                        description="You cannot ban the server owner.",
                        color=0xE02B2B,
                    ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
                else:
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
                
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description="An unexpected error occurred.",
                color=0xE02B2B,
            ).set_author(name="Moderation", icon_url="https://yes.nighty.works/raw/CPKHQd.png")    
            await context.send(embed=embed, ephemeral=True)

    async def delete_all_user_messages(self, guild: discord.Guild, user_id: int) -> None:
        for channel in guild.text_channels:
            try:
                permissions = channel.permissions_for(guild.me)
                if not (permissions.read_message_history and permissions.manage_messages):
                    continue
                
                deleted = True
                while deleted:
                    deleted = False
                    try:
                        async for message in channel.history(limit=100):
                            if message.author.id == user_id:
                                try:
                                    await message.delete()
                                    deleted = True
                                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                                    continue
                    except (discord.Forbidden, discord.HTTPException):
                        break
                        
            except (discord.Forbidden, discord.HTTPException):
                continue

    def format_delete_time(self, delete_option: str) -> str:
        time_formats = {
            "1h": "Last 1 hour",
            "6h": "Last 6 hours", 
            "12h": "Last 12 hours",
            "1d": "Last 24 hours",
            "3d": "Last 3 days",
            "7d": "Last 7 days"
        }
        return time_formats.get(delete_option, "Unknown time period")
    
    return ban