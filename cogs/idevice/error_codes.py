import json
import os
import discord
from discord import app_commands
from discord.ext import commands


def errorcodes_command():
    @commands.hybrid_command(
        name="errorcodes", description="Look up an idevice error code by name or number"
    )
    @app_commands.describe(name="Start typing to search all error names and codes")
    async def errorcodes(self, context, name: str | None = None):
        if name is None:
            if context.interaction:
                await context.interaction.response.send_message(
                    "Please provide an error code.", ephemeral=True
                )
            else:
                await context.send("Please provide an error code.")
            return

        def load_errors():
            json_path = os.path.join(os.path.dirname(__file__), "files/errorcodes.json")
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                self.bot.logger.error(f"Error codes JSON file not found: {json_path}")
                return []
            except json.JSONDecodeError as e:
                self.bot.logger.error(f"Error parsing error codes JSON: {e}")
                return []

        errors = load_errors()
        key_to_data = {
            error["name"]: (error["description"], error["code"]) for error in errors
        }
        code_to_key = {error["code"]: error["name"] for error in errors}

        key = name
        if key not in key_to_data:
            try:
                num = int(name)
                key = code_to_key.get(num)
                if key is None and num > 0:
                    key = code_to_key.get(-num)
            except ValueError:
                key = None
        if key is None or key not in key_to_data:
            if context.interaction:
                await context.interaction.response.send_message(
                    "Error not found.", ephemeral=True
                )
            else:
                await context.send("Error not found.")
            return

        title, code = key_to_data[key]

        embed = discord.Embed(
            description=f"## Error Code: {code}\n\n**Name**: `{key}`\n**Description**: {title}",
            color=0xFA8C4A,
        )
        embed.set_author(
            name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png"
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Edit Command",
                style=discord.ButtonStyle.secondary,
                url="https://github.com/neoarz/Syntrel/blob/main/cogs/idevice/error_codes.py",
                emoji="<:githubicon:1417717356846776340>",
            )
        )

        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

    return errorcodes
