import asyncio
import io
import tempfile
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS


DEFAULT_LANG = "en"

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

def tts_command():

    async def send_embed(
        context: commands.Context,
        embed: discord.Embed,
        *,
        ephemeral: bool = False,
        file: Optional[discord.File] = None,
    ) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                if file:
                    await interaction.followup.send(embed=embed, file=file, ephemeral=ephemeral)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                if file:
                    await interaction.response.send_message(embed=embed, file=file, ephemeral=ephemeral)
                else:
                    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            if file:
                await context.send(embed=embed, file=file)
            else:
                await context.send(embed=embed)

    async def generate_tts_audio(text: str) -> tuple[Optional[bytes], Optional[str]]:
        try:
            loop = asyncio.get_event_loop()
            audio_bytes = await loop.run_in_executor(
                None,
                lambda: _generate_tts_sync(text)
            )
            return audio_bytes, None
        except Exception as e:
            return None, str(e)

    def _generate_tts_sync(text: str) -> bytes:
        tts = gTTS(text=text, lang=DEFAULT_LANG, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()

    @commands.hybrid_command(
        name="tts",
        description="Convert text to speech using Google Text-to-Speech.",
    )
    @app_commands.describe(
        text="The text to convert to speech",
    )
    async def tts(context: commands.Context, text: Optional[str] = None):
        if not text or not text.strip():
            if context.message and context.message.reference and context.message.reference.resolved:
                referenced = context.message.reference.resolved
                if isinstance(referenced, discord.Message) and referenced.content:
                    text = referenced.content
        if not text or not text.strip():
            await send_error_message(context, "Please provide text to convert or reply to a message containing text.")
            return

        text = text.strip()
        if len(text) > 500:
            await send_error_message(context, "Text is too long. Please limit to 500 characters.")
            return

        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=False)
        else:
            processing_embed = (
                discord.Embed(
                    title="TTS (Processing)",
                    description="<a:mariospin:1423677027013103709> Generating speech...",
                    color=0x7289DA,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            )
            processing_message = await context.send(embed=processing_embed)

        audio_bytes, error = await generate_tts_audio(text)

        if error or not audio_bytes:
            if interaction is not None:
                await interaction.followup.send(embed=discord.Embed(
                    title="Error",
                    description=f"Failed to generate speech. {error or 'Unknown error.'}",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"), ephemeral=True)
            else:
                await processing_message.delete()
                await context.send(embed=discord.Embed(
                    title="Error",
                    description=f"Failed to generate speech. {error or 'Unknown error.'}",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"), ephemeral=True)
            return

        audio_file = discord.File(
            io.BytesIO(audio_bytes),
            filename="audio.mp3",
        )

        embed = (
            discord.Embed(
                title="Text-to-Speech",
                description=f"**Input:** {text}",
                color=0x7289DA,
            )
            .set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            .set_footer(
                text=f"Requested by {context.author.display_name}",
                icon_url=getattr(context.author.display_avatar, "url", None),
            )
        )

        if interaction is not None:
            await interaction.followup.send(embeds=[embed], files=[audio_file])
        else:
            await processing_message.delete()
            await context.send(embeds=[embed], files=[audio_file])

    return tts
