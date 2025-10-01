import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import re
import json


def codepreview_command():
    LANGUAGE_MAP = {
        '.py': 'python',
        '.js': 'js',
        '.ts': 'ts',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'cs',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.ini': 'ini',
        '.toml': 'toml',
        '.lua': 'lua',
        '.sh': 'bash',
        '.md': 'markdown',
        '.sql': 'sql',
        '.diff': 'diff',
        '.txt': '',
    }

    async def send_embed(context, embed: discord.Embed, *, ephemeral: bool = False) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await context.send(embed=embed)

    def get_language_from_filename(filename):
        for ext, lang in LANGUAGE_MAP.items():
            if filename.endswith(ext):
                return lang
        return ''

    async def fetch_github_content(url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
        except Exception:
            pass
        return None

    def parse_github_url(url):
        raw_pattern = r'https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+?)$'
        raw_match = re.match(raw_pattern, url)
        
        if raw_match:
            owner, repo, branch, filepath = raw_match.groups()
            
            return {
                'owner': owner,
                'repo': repo,
                'branch': branch,
                'filepath': filepath,
                'raw_url': url,
                'start_line': None,
                'end_line': None
            }
        
        pattern = r'https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?)(?:#L(\d+)(?:-L(\d+))?)?$'
        match = re.match(pattern, url)
        
        if match:
            owner, repo, branch, filepath, start_line, end_line = match.groups()
            
            raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filepath}'
            
            return {
                'owner': owner,
                'repo': repo,
                'branch': branch,
                'filepath': filepath,
                'raw_url': raw_url,
                'start_line': int(start_line) if start_line else None,
                'end_line': int(end_line) if end_line else None
            }
        return None

    def extract_lines(content, start_line, end_line):
        lines = content.split('\n')
        
        if start_line and end_line:
            return '\n'.join(lines[start_line-1:end_line])
        elif start_line:
            return lines[start_line-1] if start_line <= len(lines) else content
        return content

    @commands.hybrid_command(
        name="codepreview",
        description="Preview code from GitHub URLs",
    )
    @app_commands.describe(
        url="GitHub URL to preview code from"
    )
    async def codepreview(self, context, url: str = None):
        if not url or not url.strip():
            if context.message and context.message.reference and context.message.reference.resolved:
                replied_message = context.message.reference.resolved
                if hasattr(replied_message, 'content') and replied_message.content:
                    github_pattern = r'https://(?:github\.com|raw\.githubusercontent\.com)/[^\s]+'
                    urls = re.findall(github_pattern, replied_message.content)
                    if urls:
                        url = urls[0]
                    else:
                        embed = discord.Embed(
                            title="Error",
                            description="No GitHub URL found in the replied message.",
                            color=0xE02B2B,
                        ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                        await send_embed(context, embed, ephemeral=True)
                        return
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="The replied message has no content to extract GitHub URL from.",
                        color=0xE02B2B,
                    ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                    await send_embed(context, embed, ephemeral=True)
                    return
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Please provide a GitHub URL or reply to a message containing a GitHub URL.",
                    color=0xE02B2B,
                ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                await send_embed(context, embed, ephemeral=True)
                return
        
        if not url.startswith('https://github.com/') and not url.startswith('https://raw.githubusercontent.com/'):
            embed = discord.Embed(
                title="Error",
                description="Please provide a valid GitHub URL.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        parsed = parse_github_url(url)
        
        if not parsed:
            embed = discord.Embed(
                title="Error",
                description="Invalid GitHub URL format. Please provide a valid GitHub blob URL.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        content = await fetch_github_content(parsed['raw_url'])
        
        if not content:
            embed = discord.Embed(
                title="Error",
                description="Failed to fetch content from GitHub. The file might not exist or be accessible.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        if parsed['start_line']:
            code = extract_lines(content, parsed['start_line'], parsed['end_line'])
            line_info = f" (Lines {parsed['start_line']}"
            if parsed['end_line']:
                line_info += f"-{parsed['end_line']}"
            line_info += ")"
        else:
            code = content
            line_info = ""
        
        filename = parsed['filepath'].split('/')[-1]
        language = get_language_from_filename(filename)
        
        embed = discord.Embed(
            title="Code Preview",
            description=f"**Repository URL:** [{parsed['owner']}/{parsed['repo']}]({url})",
            color=0x7289DA,
        )
        embed.set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        embed.add_field(name="File", value=f"`{parsed['filepath']}`{line_info}", inline=True)
        embed.add_field(name="Branch", value=f"`{parsed['branch']}`", inline=True)
        embed.set_footer(text=f"Requested by {context.author.name}", icon_url=context.author.display_avatar.url)
        
        code_block = f"```{language}\n{code}\n```"
        
        if len(code_block) > 1990:
            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.defer(ephemeral=True)
                await context.channel.send(embed=embed)
            else:
                await context.channel.send(embed=embed)
            
            max_code_length = 1980 - len(language) - 8
            code_lines = code.split('\n')
            current_chunk = []
            current_length = 0
            
            for line in code_lines:
                line_length = len(line) + 1
                if current_length + line_length > max_code_length:
                    chunk_text = '\n'.join(current_chunk)
                    if interaction is not None:
                        await context.channel.send(f"```{language}\n{chunk_text}\n```")
                    else:
                        await context.channel.send(f"```{language}\n{chunk_text}\n```")
                    current_chunk = [line]
                    current_length = line_length
                else:
                    current_chunk.append(line)
                    current_length += line_length
            
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                if interaction is not None:
                    await context.channel.send(f"```{language}\n{chunk_text}\n```")
                    try:
                        await interaction.delete_original_response()
                    except:
                        pass
                else:
                    await context.channel.send(f"```{language}\n{chunk_text}\n```")
        else:
            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.defer(ephemeral=True)
                await context.channel.send(embed=embed)
                await context.channel.send(code_block)
                try:
                    await interaction.delete_original_response()
                except:
                    pass
            else:
                await context.channel.send(embed=embed)
                await context.channel.send(code_block)

    return codepreview