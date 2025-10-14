import base64
import io
from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands


PUTER_TTS_ENDPOINT = "https://api.puter.com/v2/speech/generate"
DEFAULT_VOICE = "alloy"
SUPPORTED_FORMAT = "mp3"


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
                await interaction.followup.send(embed=embed, file=file, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, file=file, ephemeral=ephemeral)
        else:
            await context.send(embed=embed, file=file)

    async def fetch_tts_audio(text: str, voice: str) -> tuple[Optional[bytes], Optional[str]]:
        payload = {
            "input": text,
            "voice": voice,
            "format": SUPPORTED_FORMAT,
        }
        headers = {"Content-Type": "application/json"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(PUTER_TTS_ENDPOINT, json=payload, headers=headers) as response:
                    if response.status != 200:
                        try:
                            error_text = (await response.text()).strip()
                        except Exception:
                            error_text = "Unknown error"
                        return None, f"API returned {response.status}: {error_text[:200]}"

                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        data = await response.json(content_type=None)
                        audio_b64 = data.get("audio") or data.get("data")
                        if not audio_b64:
                            return None, "API response did not include audio data."
                        try:
                            audio_bytes = base64.b64decode(audio_b64)
                        except Exception:
                            return None, "Failed to decode audio data from API response."
                        return audio_bytes, None

                    audio_bytes = await response.read()
                    if not audio_bytes:
                        return None, "Received empty audio data from API."
                    return audio_bytes, None
        except aiohttp.ClientError as exc:
            return None, f"Network error while contacting TTS service: {exc}"
        except Exception as exc:  # pragma: no cover - defensive
            return None, f"Unexpected error while generating TTS: {exc}"

    @commands.hybrid_command(
        name="tts",
        description="Convert text to speech using the Puter TTS API.",
    )
    @app_commands.describe(
        text="The text to convert to speech",
        voice="Voice to use for the speech (default: alloy)",
    )
    async def tts(self, context: commands.Context, text: Optional[str] = None, voice: str = DEFAULT_VOICE):
        if voice:
            voice = voice.strip()
        if not voice:
            voice = DEFAULT_VOICE

        if not text or not text.strip():
            if context.message and context.message.reference and context.message.reference.resolved:
                referenced = context.message.reference.resolved
                if isinstance(referenced, discord.Message) and referenced.content:
                    text = referenced.content
        if not text or not text.strip():
            embed = (
                discord.Embed(
                    title="Error",
                    description="Please provide text to convert or reply to a message containing text.",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            )
            await send_embed(context, embed, ephemeral=True)
            return

        text = text.strip()
        if len(text) > 600:
            embed = (
                discord.Embed(
                    title="Error",
                    description="Text is too long. Please limit to 600 characters.",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            )
            await send_embed(context, embed, ephemeral=True)
            return

        processing_embed = (
            discord.Embed(
                title="TTS (Processing)",
                description="<a:mariospin:1423677027013103709> Generating speech...",
                color=0x7289DA,
            ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        )

        interaction = getattr(context, "interaction", None)
        followup_message = None
        if interaction is not None:
            if interaction.response.is_done():
                followup_message = await interaction.followup.send(embed=processing_embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=processing_embed, ephemeral=True)
        else:
            followup_message = await context.send(embed=processing_embed)

        audio_bytes, error = await fetch_tts_audio(text, voice)

        if error or not audio_bytes:
            embed = (
                discord.Embed(
                    title="Error",
                    description=f"Failed to generate speech. {error or 'Unknown error.'}",
                    color=0xE02B2B,
                ).set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            )
            await send_embed(context, embed, ephemeral=True)
            if followup_message:
                try:
                    await followup_message.delete()
                except Exception:
                    pass
            return

        audio_file = discord.File(
            io.BytesIO(audio_bytes),
            filename=f"tts_{voice or DEFAULT_VOICE}.{SUPPORTED_FORMAT}",
        )

        embed = (
            discord.Embed(
                title="Text-to-Speech",
                description=f"**Input:** {text}",
                color=0x2ECC71,
            )
            .set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            .set_footer(text=f"Voice: {voice or DEFAULT_VOICE}")
        )

        await send_embed(context, embed, file=audio_file)

        if followup_message:
            try:
                await followup_message.delete()
            except Exception:
                pass

    return tts
