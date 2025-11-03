import os
import tempfile
import discord
from discord.ext import commands
from PIL import Image
import subprocess
import shutil
from typing import Optional

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except Exception:
    pass


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


def img2gif_command():
    @commands.hybrid_command(
        name="img2gif",
        description="Convert an uploaded image to a GIF.",
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def img2gif(self, context, attachment: Optional[discord.Attachment] = None):
        resolved_attachment = attachment
        if resolved_attachment is None:
            if (
                context.message
                and context.message.reference
                and context.message.reference.resolved
            ):
                ref_msg = context.message.reference.resolved
                if isinstance(ref_msg, discord.Message) and ref_msg.attachments:
                    resolved_attachment = ref_msg.attachments[0]
            if (
                resolved_attachment is None
                and context.message
                and context.message.attachments
            ):
                resolved_attachment = context.message.attachments[0]
        if (
            resolved_attachment is None
            or not resolved_attachment.filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".heic", ".heif")
            )
        ):
            await send_error_message(
                context,
                "Provide or reply to an image (png/jpg/jpeg/webp/bmp/tiff/heic/heif).",
            )
            return

        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=False)
        else:
            processing_embed = discord.Embed(
                title="Image to GIF (Processing)",
                description="<a:mariospin:1423677027013103709> Converting image...",
                color=0x7289DA,
            )
            processing_embed.set_author(
                name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp"
            )
            processing_msg = await context.send(embed=processing_embed)

        tmp_dir = tempfile.mkdtemp()
        src_path = os.path.join(tmp_dir, resolved_attachment.filename)
        out_path = os.path.join(
            tmp_dir, os.path.splitext(resolved_attachment.filename)[0] + ".gif"
        )

        try:
            await resolved_attachment.save(src_path)
            src_for_pillow = src_path
            try:
                with Image.open(src_for_pillow) as img:
                    if img.mode not in ("RGB", "RGBA"):
                        img = img.convert("RGBA")
                    duration_ms = 100
                    loop = 0
                    img.save(
                        out_path,
                        format="GIF",
                        save_all=True,
                        optimize=True,
                        duration=duration_ms,
                        loop=loop,
                    )
            except Exception:
                if resolved_attachment.filename.lower().endswith(
                    (".heic", ".heif")
                ) and shutil.which("ffmpeg"):
                    png_path = os.path.join(
                        tmp_dir,
                        os.path.splitext(resolved_attachment.filename)[0] + ".png",
                    )
                    try:
                        subprocess.run(
                            ["ffmpeg", "-y", "-i", src_path, png_path],
                            check=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        with Image.open(png_path) as img:
                            if img.mode not in ("RGB", "RGBA"):
                                img = img.convert("RGBA")
                            duration_ms = 100
                            loop = 0
                            img.save(
                                out_path,
                                format="GIF",
                                save_all=True,
                                optimize=True,
                                duration=duration_ms,
                                loop=loop,
                            )
                    except Exception as conv_err:
                        raise conv_err
                else:
                    raise

            with open(out_path, "rb") as f:
                file = discord.File(f, filename=os.path.basename(out_path))
                if interaction is not None:
                    await interaction.followup.send(file=file)
                else:
                    await processing_msg.delete()
                    await context.send(file=file)
        except Exception as e:
            if interaction is not None:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"Failed to convert image: {e}",
                        color=0xE02B2B,
                    ).set_author(
                        name="Media",
                        icon_url="https://yes.nighty.works/raw/y5SEZ9.webp",
                    ),
                    ephemeral=True,
                )
            else:
                await processing_msg.delete()
                await context.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"Failed to convert image: {e}",
                        color=0xE02B2B,
                    ).set_author(
                        name="Media",
                        icon_url="https://yes.nighty.works/raw/y5SEZ9.webp",
                    ),
                    ephemeral=True,
                )
        finally:
            try:
                for f in os.listdir(tmp_dir):
                    try:
                        os.remove(os.path.join(tmp_dir, f))
                    except:
                        pass
                os.rmdir(tmp_dir)
            except:
                pass

    return img2gif
