import asyncio
import os
import tempfile
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import io
from datetime import datetime
from typing import Optional


class TweetyView(discord.ui.View):
    """ API for Tweety is hosted on Vercel and made by me :) github can be found here: https://github.com/neoarz/tweety-api"""

    def __init__(self, author_id: int, original_message, tweet_data: dict, api_url: str, image_message: Optional[discord.Message] = None):
        super().__init__(timeout=300)
        self.author_id = author_id
        self.original_message = original_message
        self.tweet_data = tweet_data
        self.api_url = api_url
        self.is_dark = tweet_data.get("dark", False)
        self.is_verified = tweet_data.get("verified", False)
        self.image_message = image_message

        self.update_button_styles()
    
    def update_button_styles(self):
        """Update button styles to reflect current state"""
        self.clear_items()
        
        dark_button = discord.ui.Button(
            label="Dark Mode" if self.is_dark else "Light Mode",
            style=discord.ButtonStyle.primary if self.is_dark else discord.ButtonStyle.secondary,
            emoji=discord.PartialEmoji(name="darkmode", id=1425165393751965884),
            custom_id="toggle_dark"
        )
        dark_button.callback = self.toggle_dark_callback
        self.add_item(dark_button)
        
        verified_button = discord.ui.Button(
            label="Verified",
            style=discord.ButtonStyle.primary if self.is_verified else discord.ButtonStyle.secondary,
            emoji=discord.PartialEmoji(name="TwitterVerifiedBadge", id=1425165432142172392),
            custom_id="toggle_verified"
        )
        verified_button.callback = self.toggle_verified_callback
        self.add_item(verified_button)
    
    async def regenerate_tweet(self, interaction: discord.Interaction):
        """Regenerate only the image message with current settings"""
        await interaction.response.defer()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/render",
                    json=self.tweet_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        embed = discord.Embed(
                            title="Error",
                            description=f"API Error ({response.status}): {error_text}",
                            color=0xE02B2B,
                        )
                        embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                        await interaction.followup.send(embed=embed, ephemeral=True)
                        return
                    
                    image_data = await response.read()
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                        temp_file.write(image_data)
                        temp_file_path = temp_file.name
                    
                    with open(temp_file_path, 'rb') as f:
                        author_name = self.original_message.author.name
                        filename = f"tweet_{author_name}_{int(datetime.now().timestamp())}.png"
                        file = discord.File(
                            f, 
                            filename=filename
                        )

                        self.update_button_styles()

                        if self.image_message is not None:
                            await self.image_message.edit(attachments=[file], view=self)
                        else:
                            await interaction.followup.send(file=file, view=self)
                    
                    os.remove(temp_file_path)
                    
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="Error regenerating tweet image",
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def toggle_dark_callback(self, interaction: discord.Interaction):
        """Handle dark mode toggle button click"""
        if interaction.user.id != self.author_id:
            embed = discord.Embed(
                title="Error",
                description="You can't modify someone else's tweet!",
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        self.is_dark = not self.is_dark
        self.tweet_data["dark"] = self.is_dark
        
        await self.regenerate_tweet(interaction)
    
    async def toggle_verified_callback(self, interaction: discord.Interaction):
        """Handle verified toggle button click"""
        if interaction.user.id != self.author_id:
            embed = discord.Embed(
                title="Error",
                description="You can't modify someone else's tweet!",
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        self.is_verified = not self.is_verified
        self.tweet_data["verified"] = self.is_verified
        
        await self.regenerate_tweet(interaction)
    
    async def on_timeout(self):
        """Disable buttons when view times out"""
        for item in self.children:
            item.disabled = True
        
        try:
            pass
        except:
            pass

def tweety_command():
    @commands.hybrid_command(
        name="tweety",
        description="Convert a replied message to a tweet image."
    )
    @app_commands.describe(
        verified="Add a verified badge to the tweet",
        theme="Choose the theme for the tweet"
    )
    @app_commands.choices(verified=[
        app_commands.Choice(name="No", value="false"),
        app_commands.Choice(name="Yes", value="true")
    ])
    @app_commands.choices(theme=[
        app_commands.Choice(name="Light", value="light"),
        app_commands.Choice(name="Dark", value="dark")
    ])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tweety(self, context, verified: Optional[str] = "false", theme: Optional[str] = "light"):
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            try:
                embed = discord.Embed(
                    title="Tweety",
                    description=(
                        "Use the prefix command: `.media tweety`\n"
                        f"Or reply to a message with: <@{self.bot.user.id}> tweety"
                    ),
                    color=0x7289DA,
                )
                embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)
            except Exception:
                pass
            return
        verified_bool = verified == "true"
        theme_bool = theme == "dark"
        
        if not context.message.reference or not context.message.reference.message_id:
            embed = discord.Embed(
                title="Error",
                description="You must reply to a message to use this command!",
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            
            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await context.send(embed=embed, ephemeral=True)
            return
        
        original_message = await context.channel.fetch_message(context.message.reference.message_id)
        
        try:
            if not original_message:
                embed = discord.Embed(
                    title="Error",
                    description="Could not find the original message!",
                    color=0xE02B2B,
                )
                embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                
                interaction = getattr(context, "interaction", None)
                if interaction is not None:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await context.send(embed=embed, ephemeral=True)
                return
            
            if original_message.author.bot:
                embed = discord.Embed(
                    title="Error",
                    description="Cannot convert bot messages to tweets!",
                    color=0xE02B2B,
                )
                embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                
                interaction = getattr(context, "interaction", None)
                if interaction is not None:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await context.send(embed=embed, ephemeral=True)
                return

            processing_embed = discord.Embed(
                title="Tweet Generator (Processing)",
                description="<a:mariospin:1423677027013103709> Generating tweet... This may take a moment.",
                color=0x7289DA,
            )
            processing_embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            
            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=processing_embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=processing_embed, ephemeral=True)
            else:
                processing_msg = await context.send(embed=processing_embed)

            author = original_message.author
            display_name = author.display_name or author.name
            username = f"@{author.name}"
            avatar_url = str(author.avatar.url) if author.avatar else str(author.default_avatar.url)
            message_text = original_message.content
            
            image_url = None
            if original_message.attachments:
                for attachment in original_message.attachments:
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        raw_url = attachment.url
                        if 'cdn.discordapp.com' in raw_url:
                            media_url = raw_url.replace('cdn.discordapp.com', 'media.discordapp.net')
                            if '?' not in media_url:
                                media_url += f"?width={attachment.width}&height={attachment.height}"
                            elif 'width=' not in media_url and attachment.width:
                                media_url += f"&width={attachment.width}&height={attachment.height}"
                            image_url = media_url
                        else:
                            image_url = raw_url
                        break
            
            if not message_text.strip() and not image_url:
                embed = discord.Embed(
                    title="Error",
                    description="Message must have either text content or an image/GIF to convert!",
                    color=0xE02B2B,
                )
                embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                
                interaction = getattr(context, "interaction", None)
                if interaction is not None:
                    try:
                        await interaction.delete_original_response()
                    except:
                        pass
                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await processing_msg.delete()
                    await context.send(embed=embed, ephemeral=True)
                return
            
            msg_time = original_message.created_at
            timestamp = msg_time.strftime("%I:%M %p · %b %d, %Y").replace(" 0", " ")
            
            tweet_data = {
                "name": display_name[:50],
                "handle": username[:20],
                "text": message_text[:300],
                "avatar": avatar_url,
                "timestamp": timestamp,
                "verified": verified_bool,
                "dark": theme_bool
            }
            
            if image_url:
                tweet_data["image"] = image_url
            
            API_BASE_URL = "https://tweety-api.vercel.app"
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        f"{API_BASE_URL}/api/render",
                        json=tweet_data,
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        
                        if response.status != 200:
                            error_text = await response.text()
                            embed = discord.Embed(
                                title="Error",
                                description=f"API Error ({response.status}): {error_text}",
                                color=0xE02B2B,
                            )
                            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                            
                            interaction = getattr(context, "interaction", None)
                            if interaction is not None:
                                try:
                                    await interaction.delete_original_response()
                                except:
                                    pass
                                await interaction.followup.send(embed=embed, ephemeral=True)
                            else:
                                await processing_msg.delete()
                                await context.send(embed=embed, ephemeral=True)
                            return
                        
                        image_data = await response.read()
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                            temp_file.write(image_data)
                            temp_file_path = temp_file.name

                        with open(temp_file_path, 'rb') as f:
                            file = discord.File(f, filename=f"tweet_{author.name}_{int(datetime.now().timestamp())}.png")
                            embed = discord.Embed(
                                title="Tweet Generated",
                                color=0x7289DA,
                            )
                            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                            embed.set_footer(
                                text=f"Requested by {context.author.name}",
                                icon_url=context.author.display_avatar.url,
                            )

                            view = TweetyView(
                                author_id=context.author.id,
                                original_message=original_message,
                                tweet_data=tweet_data,
                                api_url=API_BASE_URL
                            )

                            interaction = getattr(context, "interaction", None)
                            if interaction is not None:
                                embed_message = await context.channel.send(embed=embed)
                                image_message = await context.channel.send(file=file, view=view)
                                view.image_message = image_message
                                try:
                                    await interaction.delete_original_response()
                                except:
                                    pass
                            else:
                                await processing_msg.delete()
                                embed_message = await context.channel.send(embed=embed)
                                image_message = await context.channel.send(file=file, view=view)
                                view.image_message = image_message

                        os.remove(temp_file_path)
                        
                except aiohttp.ClientError as e:
                    embed = discord.Embed(
                        title="Error",
                        description=f"Connection error: Could not reach tweet API at {API_BASE_URL}",
                        color=0xE02B2B,
                    )
                    embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                    
                    interaction = getattr(context, "interaction", None)
                    if interaction is not None:
                        try:
                            await interaction.delete_original_response()
                        except:
                            pass
                        await interaction.followup.send(embed=embed, ephemeral=True)
                    else:
                        await processing_msg.delete()
                        await context.send(embed=embed, ephemeral=True)
                except Exception as e:
                    embed = discord.Embed(
                        title="Error",
                        description="Error generating tweet image",
                        color=0xE02B2B,
                    )
                    embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                    
                    interaction = getattr(context, "interaction", None)
                    if interaction is not None:
                        try:
                            await interaction.delete_original_response()
                        except:
                            pass
                        await interaction.followup.send(embed=embed, ephemeral=True)
                    else:
                        await processing_msg.delete()
                        await context.send(embed=embed, ephemeral=True)
                   
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="Error processing the message!",
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            
            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await context.send(embed=embed, ephemeral=True)
    
    return tweety
