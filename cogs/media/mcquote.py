import asyncio
import os
import tempfile
import discord
from discord.ext import commands
import aiohttp
import random

async def send_error_message(context, description: str):
    embed = discord.Embed(
        title="Error",
        description=description,
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

def mcquote_command():
    @commands.hybrid_command(
        name="mcquote",
        description="Generate a custom Minecraft quote image.",
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mcquote(self, context, *, text: str = None):
        if not text:
            await send_error_message(context, "Please provide text for the Minecraft quote.")
            return

        if len(text) > 25:
            await send_error_message(context, "Text must be 25 characters or less.")
            return

        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=False)
        else:
            processing_embed = discord.Embed(
                title="Minecraft Quote (Processing)",
                description="<a:mariospin:1423677027013103709> Generating quote... This may take a moment.",
                color=0x7289DA,
            )
            processing_embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
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
                
                if interaction is not None:
                    await interaction.followup.send(embeds=[embed], files=[file])
                else:
                    await processing_msg.delete()
                    await context.send(embeds=[embed], files=[file])

            os.remove(temp_file_path)
        except aiohttp.ClientError:
            if interaction is not None:
                await interaction.followup.send(embed=discord.Embed(
                    title="Error",
                    description="Failed to generate Minecraft quote. Please try again later.",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"), ephemeral=True)
            else:
                await processing_msg.delete()
                await context.send(embed=discord.Embed(
                    title="Error",
                    description="Failed to generate Minecraft quote. Please try again later.",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"), ephemeral=True)
        except Exception as e:
            if interaction is not None:
                await interaction.followup.send(embed=discord.Embed(
                    title="Error",
                    description=f"An unexpected error occurred: {str(e)}",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"), ephemeral=True)
            else:
                await processing_msg.delete()
                await context.send(embed=discord.Embed(
                    title="Error",
                    description=f"An unexpected error occurred: {str(e)}",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"), ephemeral=True)
    
    return mcquote
