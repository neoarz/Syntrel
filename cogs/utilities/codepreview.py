import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import re
import json


def codepreview_command():
    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "js",
        ".ts": "ts",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "cs",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".xml": "xml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".ini": "ini",
        ".toml": "toml",
        ".lua": "lua",
        ".sh": "bash",
        ".md": "markdown",
        ".sql": "sql",
        ".diff": "diff",
        ".txt": "",
    }

    async def send_embed(
        context, embed: discord.Embed, *, ephemeral: bool = False
    ) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(
                    embed=embed, ephemeral=ephemeral
                )
        else:
            await context.send(embed=embed)

    def get_language_from_filename(filename):
        for ext, lang in LANGUAGE_MAP.items():
            if filename.endswith(ext):
                return lang
        return ""

    async def fetch_github_content(url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
        except Exception:
            pass
        return None

    async def fetch_pr_diff(owner, repo, pr_number):
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
            headers = {
                "Accept": "application/vnd.github.v3.diff",
                "User-Agent": "Discord-Bot",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    if response.status == 200:
                        diff_content = await response.text()
                        return diff_content
        except Exception:
            pass
        return None

    async def fetch_pr_info(owner, repo, pr_number):
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Discord-Bot",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    if response.status == 200:
                        pr_data = await response.json()
                        return {
                            "title": pr_data.get("title", ""),
                            "number": pr_data.get("number", pr_number),
                            "state": pr_data.get("state", ""),
                            "merged": pr_data.get("merged", False),
                            "additions": pr_data.get("additions", 0),
                            "deletions": pr_data.get("deletions", 0),
                            "changed_files": pr_data.get("changed_files", 0),
                            "user": pr_data.get("user", {}).get("login", ""),
                            "base_branch": pr_data.get("base", {}).get("ref", ""),
                            "head_branch": pr_data.get("head", {}).get("ref", ""),
                        }
        except Exception:
            pass
        return None

    def parse_github_url(url):
        pr_pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)(?:/files)?"
        pr_match = re.match(pr_pattern, url)

        if pr_match:
            owner, repo, pr_number = pr_match.groups()
            return {"type": "pr", "owner": owner, "repo": repo, "pr_number": pr_number}

        raw_pattern = (
            r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+?)$"
        )
        raw_match = re.match(raw_pattern, url)

        if raw_match:
            owner, repo, branch, filepath = raw_match.groups()

            return {
                "type": "file",
                "owner": owner,
                "repo": repo,
                "branch": branch,
                "filepath": filepath,
                "raw_url": url,
                "start_line": None,
                "end_line": None,
            }

        pattern = r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?)(?:#L(\d+)(?:-L(\d+))?)?$"
        match = re.match(pattern, url)

        if match:
            owner, repo, branch, filepath, start_line, end_line = match.groups()

            raw_url = (
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filepath}"
            )

            return {
                "type": "file",
                "owner": owner,
                "repo": repo,
                "branch": branch,
                "filepath": filepath,
                "raw_url": raw_url,
                "start_line": int(start_line) if start_line else None,
                "end_line": int(end_line) if end_line else None,
            }
        return None

    def extract_lines(content, start_line, end_line):
        lines = content.split("\n")

        if start_line and end_line:
            return "\n".join(lines[start_line - 1 : end_line])
        elif start_line:
            return lines[start_line - 1] if start_line <= len(lines) else content
        return content

    @commands.hybrid_command(
        name="codepreview",
        description="Preview code from GitHub URLs",
    )
    @app_commands.describe(url="GitHub URL to preview code from")
    async def codepreview(self, context, url: str = None):
        if isinstance(context.channel, discord.DMChannel):
            embed = discord.Embed(
                title="Error",
                description="This command can only be used in servers.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )

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
            embed.set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )

            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await context.send(embed=embed, ephemeral=True)
            return

        if not url or not url.strip():
            if (
                context.message
                and context.message.reference
                and context.message.reference.resolved
            ):
                replied_message = context.message.reference.resolved
                if hasattr(replied_message, "content") and replied_message.content:
                    github_pattern = (
                        r"https://(?:github\.com|raw\.githubusercontent\.com)/[^\s]+"
                    )
                    urls = re.findall(github_pattern, replied_message.content)
                    if urls:
                        url = urls[0]
                    else:
                        embed = discord.Embed(
                            title="Error",
                            description="No GitHub URL found in the replied message.",
                            color=0xE02B2B,
                        ).set_author(
                            name="Utility",
                            icon_url="https://yes.nighty.works/raw/8VLDcg.webp",
                        )
                        await send_embed(context, embed, ephemeral=True)
                        return
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="The replied message has no content to extract GitHub URL from.",
                        color=0xE02B2B,
                    ).set_author(
                        name="Utility",
                        icon_url="https://yes.nighty.works/raw/8VLDcg.webp",
                    )
                    await send_embed(context, embed, ephemeral=True)
                    return
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Please provide a GitHub URL or reply to a message containing a GitHub URL.",
                    color=0xE02B2B,
                ).set_author(
                    name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
                )
                await send_embed(context, embed, ephemeral=True)
                return

        if not url.startswith("https://github.com/") and not url.startswith(
            "https://raw.githubusercontent.com/"
        ):
            embed = discord.Embed(
                title="Error",
                description="Please provide a valid GitHub URL.",
                color=0xE02B2B,
            ).set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )
            await send_embed(context, embed, ephemeral=True)
            return

        # Check if bot has send messages permission before starting processing
        try:
            test_embed = discord.Embed(title="Testing permissions...", color=0x7289DA)
            test_embed.set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )
            await context.channel.send(embed=test_embed, delete_after=0.1)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Permission Error",
                description="The bot needs the `send messages` permission to execute this command.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )

            interaction = getattr(context, "interaction", None)
            if interaction is not None:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await context.send(embed=embed, ephemeral=True)
            return

        parsed = parse_github_url(url)

        if not parsed:
            embed = discord.Embed(
                title="Error",
                description="Invalid GitHub URL format. Please provide a valid GitHub blob URL or PR URL.",
                color=0xE02B2B,
            ).set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )
            await send_embed(context, embed, ephemeral=True)
            return

        if parsed.get("type") == "pr":
            pr_info = await fetch_pr_info(
                parsed["owner"], parsed["repo"], parsed["pr_number"]
            )
            diff_content = await fetch_pr_diff(
                parsed["owner"], parsed["repo"], parsed["pr_number"]
            )

            if not pr_info or not diff_content:
                embed = discord.Embed(
                    title="Error",
                    description="Failed to fetch pull request information. The PR might not exist or be accessible.",
                    color=0xE02B2B,
                ).set_author(
                    name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
                )
                await send_embed(context, embed, ephemeral=True)
                return

            pr_url = f"https://github.com/{parsed['owner']}/{parsed['repo']}/pull/{parsed['pr_number']}"

            if pr_info["merged"]:
                pr_color = 0x6F42C1
                pr_status = "Merged"
            elif pr_info["state"] == "open":
                pr_color = 0x57F287
                pr_status = "Open"
            else:
                pr_color = 0xE02B2B
                pr_status = "Closed"

            embed = discord.Embed(
                title=f"Pull Request #{pr_info['number']}: {pr_info['title'][:100]}",
                description=f"**Repository:** [{parsed['owner']}/{parsed['repo']}]({pr_url})\n**Author:** {pr_info['user']}\n**Status:** {pr_status}",
                color=pr_color,
            )
            embed.set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )
            embed.add_field(
                name="Changes",
                value=f"**+{pr_info['additions']}** / **-{pr_info['deletions']}**",
                inline=True,
            )
            embed.add_field(
                name="Files Changed", value=f"{pr_info['changed_files']}", inline=True
            )
            embed.add_field(
                name="Branches",
                value=f"`{pr_info['base_branch']}` ← `{pr_info['head_branch']}`",
                inline=False,
            )
            embed.set_footer(
                text=f"Requested by {context.author.name}",
                icon_url=context.author.display_avatar.url,
            )

            interaction = getattr(context, "interaction", None)
            if interaction is not None and not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)

            await context.channel.send(embed=embed)

            max_diff_length = 1900
            max_lines = 100

            diff_lines = diff_content.split("\n")

            if len(diff_lines) > max_lines:
                diff_lines = diff_lines[:max_lines]
                diff_lines.append(
                    f"\n... ({len(diff_content.split(chr(10))) - max_lines} more lines omitted)"
                )

            current_chunk = ""

            for line in diff_lines:
                test_chunk = current_chunk + line + "\n"

                if len(test_chunk) + 10 > max_diff_length:
                    if current_chunk.strip():
                        remaining_lines = len(diff_lines) - len(
                            current_chunk.split("\n")
                        )
                        if remaining_lines > 0:
                            current_chunk += (
                                f"\n... ({remaining_lines} more lines omitted)"
                            )
                        await context.channel.send(
                            f"```diff\n{current_chunk.rstrip()}\n```"
                        )
                    break
                else:
                    current_chunk = test_chunk
            else:
                if current_chunk.strip():
                    await context.channel.send(
                        f"```diff\n{current_chunk.rstrip()}\n```"
                    )

            if interaction is not None:
                try:
                    await interaction.delete_original_response()
                except:
                    pass
            return

        content = await fetch_github_content(parsed["raw_url"])

        if not content:
            embed = discord.Embed(
                title="Error",
                description="Failed to fetch content from GitHub. The file might not exist or be accessible.",
                color=0xE02B2B,
            ).set_author(
                name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
            )
            await send_embed(context, embed, ephemeral=True)
            return

        if parsed["start_line"]:
            code = extract_lines(content, parsed["start_line"], parsed["end_line"])
            line_info = f" (Lines {parsed['start_line']}"
            if parsed["end_line"]:
                line_info += f"-{parsed['end_line']}"
            line_info += ")"
        else:
            code = content
            line_info = ""

        code_lines = code.split("\n")
        if len(code_lines) > 100:
            code = "\n".join(code_lines[:100])
            code += f"\n\n... ({len(code_lines) - 100} more lines omitted)"

        filename = parsed["filepath"].split("/")[-1]
        language = get_language_from_filename(filename)

        embed = discord.Embed(
            title="Code Preview",
            description=f"**Repository URL:** [{parsed['owner']}/{parsed['repo']}]({url})",
            color=0x7289DA,
        )
        embed.set_author(
            name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp"
        )
        embed.add_field(
            name="File", value=f"`{parsed['filepath']}`{line_info}", inline=True
        )
        embed.add_field(name="Branch", value=f"`{parsed['branch']}`", inline=True)
        embed.set_footer(
            text=f"Requested by {context.author.name}",
            icon_url=context.author.display_avatar.url,
        )

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
            code_lines = code.split("\n")
            current_chunk = []
            current_length = 0

            for line in code_lines:
                line_length = len(line) + 1
                if current_length + line_length > max_code_length:
                    remaining_lines = len(code_lines) - len(current_chunk)
                    if remaining_lines > 0:
                        current_chunk.append(
                            f"\n... ({remaining_lines} more lines omitted)"
                        )
                    chunk_text = "\n".join(current_chunk)
                    await context.channel.send(f"```{language}\n{chunk_text}\n```")
                    break
                else:
                    current_chunk.append(line)
                    current_length += line_length
            else:
                if current_chunk:
                    chunk_text = "\n".join(current_chunk)
                    await context.channel.send(f"```{language}\n{chunk_text}\n```")

            if interaction is not None:
                try:
                    await interaction.delete_original_response()
                except:
                    pass
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
