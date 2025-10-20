import asyncio
import os
import tempfile
import discord
from discord.ext import commands
import aiohttp
import random

def mcquote_command():
    @commands.hybrid_command(
        name="mcquote",
        description="Generate a custom Minecraft quote image.",
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mcquote(self, context, *, text: str = None):
        if isinstance(context.channel, discord.DMChannel):
            embed = discord.Embed(
                title="Error",
                description="This command can only be used in servers.",
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

        if isinstance(context.channel, discord.PartialMessageable):
            embed = discord.Embed(
                title="Error",
                description="The bot needs the `send messages` permission in this channel.",
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

        if not text:
            embed = discord.Embed(
                title="Error",
                description="Please provide text for the Minecraft quote.",
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

        if len(text) > 25:
            embed = discord.Embed(
                title="Error",
                description="Text must be 25 characters or less.",
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

        # Check if bot has send messages permission before starting quote generation
        try:
            test_embed = discord.Embed(title="Testing permissions...", color=0x7289DA)
            test_embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            await context.channel.send(embed=test_embed, delete_after=0.1)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Permission Error",
                description="The bot needs the `send messages` permission to execute this command.",
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
            title="Minecraft Quote (Processing)",
            description="<a:mariospin:1423677027013103709> Generating quote... This may take a moment.",
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

        quote_text = text.replace(" ", "+")
        random_number = random.randint(1, 39)
        mc_quote_url = f'https://skinmc.net/achievement/{random_number}/Achievement+Unlocked!/{quote_text}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(mc_quote_url) as response:
                    response.raise_for_status()
                    content = await response.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            embed = discord.Embed(
                title="Minecraft Quote",
                color=0x7289DA,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            embed.set_footer(text=f"Requested by {context.author.name}", icon_url=context.author.display_avatar.url)

            with open(temp_file_path, 'rb') as f:
                file = discord.File(f, filename="mcquote.png")
                
                interaction = getattr(context, "interaction", None)
                if interaction is not None:
                    await context.channel.send(embed=embed)
                    await context.channel.send(file=file)
                    try:
                        await interaction.delete_original_response()
                    except:
                        pass
                else:
                    await processing_msg.delete()
                    await context.channel.send(embed=embed)
                    await context.channel.send(file=file)

            os.remove(temp_file_path)
        except aiohttp.ClientError:
            embed = discord.Embed(
                title="Error",
                description="Failed to generate Minecraft quote. Please try again later.",
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
                description=f"An unexpected error occurred: {str(e)}",
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
    
    return mcquote