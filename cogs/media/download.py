import asyncio
import os
import tempfile
import discord
from discord.ext import commands
import yt_dlp
from urllib.parse import urlparse
import aiohttp
import logging

logger = logging.getLogger("discord_bot")

def download_command():
    @commands.hybrid_command(
        name="download",
        description="Download a video from a URL using yt-dlp.",
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def download(self, context, *, url: str):
        if not url:
            embed = discord.Embed(
                title="Error",
                description="Please provide a valid URL to download.",
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

        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                embed = discord.Embed(
                    title="Error",
                    description="Please provide a valid URL.",
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
        except Exception:
            embed = discord.Embed(
                title="Error",
                description="Please provide a valid URL.",
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
            title="Download (Processing)",
            description="Downloading video... This may take a moment.",
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

        temp_dir = tempfile.mkdtemp()
        temp_cookie_file = None
        
        ydl_opts = {
            'format': 'bestvideo[filesize<200M]+bestaudio[filesize<200M]/best[filesize<200M]/bestvideo+bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'extract_flat': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'writethumbnail': False,
            'ignoreerrors': False,
            'merge_output_format': 'mp4',
        }

        cookie_file_env = os.getenv('YTDLP_COOKIE_FILE') or os.getenv('YT_DLP_COOKIE_FILE')
        cookies_text_env = os.getenv('YTDLP_COOKIES') or os.getenv('YT_DLP_COOKIES')

        resolved_cookie_path = None
        if cookie_file_env:
            resolved_cookie_path = cookie_file_env
        elif cookies_text_env:
            try:
                fd, temp_cookie_file = tempfile.mkstemp(prefix='yt_cookies_', text=True)
                with os.fdopen(fd, 'w') as tmpf:
                    tmpf.write(cookies_text_env)
                resolved_cookie_path = temp_cookie_file
            except Exception:
                temp_cookie_file = None
        else:
            default_local_cookie = os.path.join(os.path.dirname(__file__), 'files', 'cookies.txt')
            resolved_cookie_path = default_local_cookie

        if not (resolved_cookie_path and os.path.exists(resolved_cookie_path)):
            embed = discord.Embed(
                title="Error",
                description=(
                    "Cookies file not found. Provide one via `YTDLP_COOKIE_FILE` or place a file at "
                    "`cogs/media/files/cookies.txt`."
                ),
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await context.send(embed=embed, ephemeral=True)
            return

        ydl_opts['cookiefile'] = resolved_cookie_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: ydl.extract_info(url, download=True)
                )
                
                if not info:
                    raise Exception("Could not extract video information")
                
                video_title = info.get('title', 'Unknown Title')
                video_duration_seconds = int(info.get('duration') or 0)
                video_uploader = info.get('uploader', 'Unknown')
                video_url = info.get('webpage_url') or info.get('original_url') or url
                platform = info.get('extractor') or info.get('extractor_key') or 'Unknown'
                view_count = info.get('view_count')
                
                files = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
                
                if not files:
                    raise Exception("No video file was downloaded")
                
                video_file = os.path.join(temp_dir, files[0])
                file_size = os.path.getsize(video_file)
                
                if file_size > 25 * 1024 * 1024:
                    async def upload_to_catbox(path: str) -> str:
                        try:
                            file_size_bytes = os.path.getsize(path)
                        except Exception:
                            file_size_bytes = -1
                        logger.info(f"Catbox upload start: name={os.path.basename(path)} size={file_size_bytes}")
                        form = aiohttp.FormData()
                        form.add_field('reqtype', 'fileupload')
                        form.add_field('fileToUpload', open(path, 'rb'), filename=os.path.basename(path))
                        timeout = aiohttp.ClientTimeout(total=600)
                        async with aiohttp.ClientSession(timeout=timeout) as session:
                            async with session.post('https://catbox.moe/user/api.php', data=form) as resp:
                                text = await resp.text()
                                logger.info(f"Catbox response: status={resp.status} body_len={len(text)}")
                                if resp.status == 200 and text.startswith('https://'):
                                    url_text = text.strip()
                                    logger.info(f"Catbox upload success: url={url_text}")
                                    return url_text
                                logger.error(f"Catbox upload failed: status={resp.status} body={text.strip()[:500]}")
                                raise RuntimeError(f"Upload failed: {text.strip()}")

                    try:
                        link = await upload_to_catbox(video_file)
                        minutes, seconds = divmod(video_duration_seconds, 60)
                        duration_str = f"{minutes}:{seconds:02d}"
                        description_text = f"### **[{video_title}]({video_url})**" if video_url else f"### **{video_title}**"
                        embed = discord.Embed(
                            title="Download",
                            description=description_text,
                            color=0x7289DA,
                        )
                        embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                        embed.add_field(name="Uploader", value=video_uploader or "Unknown", inline=True)
                        embed.add_field(name="Duration", value=duration_str, inline=True)
                        embed.add_field(name="Platform", value=platform, inline=True)
                        embed.set_footer(text=f"Requested by {context.author.name}", icon_url=context.author.display_avatar.url)
                        
                        if interaction is not None:
                            await context.channel.send(embed=embed)
                            await context.channel.send(link)
                            try:
                                await interaction.delete_original_response()
                            except:
                                pass
                        else:
                            await processing_msg.delete()
                            await context.channel.send(embed=embed)
                            await context.channel.send(link)
                        return
                    except Exception as upload_error:
                        logger.exception(f"Catbox upload exception: {upload_error}")
                        error_msg = str(upload_error)
                        if "greater than 200mb" in error_msg.lower():
                            description = "The video is too large to upload. The file exceeds 200MB (Catbox limit) and cannot be sent via Discord (25MB limit)."
                        else:
                            description = f"The video is over 25MB and upload to hosting failed: {upload_error}"
                        
                        embed = discord.Embed(
                            title="Error",
                            description=description,
                            color=0xE02B2B,
                        )
                        embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                        
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
                
                minutes, seconds = divmod(video_duration_seconds, 60)
                duration_str = f"{minutes}:{seconds:02d}"
                description_text = f"### **[{video_title}]({video_url})**" if video_url else f"### **{video_title}**"
                embed = discord.Embed(
                    title="Download",
                    description=description_text,
                    color=0x7289DA,
                )
                embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
                embed.add_field(name="Uploader", value=video_uploader or "Unknown", inline=True)
                embed.add_field(name="Duration", value=duration_str, inline=True)
                embed.add_field(name="Platform", value=platform, inline=True)
                embed.set_footer(text=f"Requested by {context.author.name}", icon_url=context.author.display_avatar.url)
                
                with open(video_file, 'rb') as f:
                    file = discord.File(f, filename=files[0])
                    
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
                        
        except Exception as e:
            err_text = str(e)
            needs_cookies = ('Sign in to confirm' in err_text) or ('cookies' in err_text.lower()) or ('consent' in err_text.lower())
            if needs_cookies:
                extra = "\n\nThis source may require authentication. Provide cookies via env: `YTDLP_COOKIE_FILE` (path) or `YTDLP_COOKIES` (contents). See: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp"
            else:
                extra = ""
            embed = discord.Embed(
                title="Error",
                description=f"Failed to download video: {err_text}{extra}",
                color=0xE02B2B,
            )
            embed.set_author(name="Media", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            
            if interaction is not None:
                try:
                    await interaction.delete_original_response()
                except:
                    pass
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                try:
                    await processing_msg.delete()
                except:
                    pass
                await context.send(embed=embed, ephemeral=True)
        
        finally:
            for file in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass
            if temp_cookie_file:
                try:
                    os.remove(temp_cookie_file)
                except:
                    pass
    
    return download