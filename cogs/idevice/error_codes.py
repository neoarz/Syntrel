import json
import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class ErrorCodes(commands.Cog, name="errorcodes"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.errors = self.load_errors()
        self.key_to_data = {error['name']: (error['description'], error['code']) for error in self.errors}
        self.code_to_key = {error['code']: error['name'] for error in self.errors}

    def load_errors(self):
        json_path = os.path.join(os.path.dirname(__file__), 'files/errorcodes.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.bot.logger.error(f"Error codes JSON file not found: {json_path}")
            return []
        except json.JSONDecodeError as e:
            self.bot.logger.error(f"Error parsing error codes JSON: {e}")
            return []

    async def errorcode_autocomplete(self, interaction: discord.Interaction, current: str):
        current_lower = current.lower()
        items = []
        for key, (title, code) in self.key_to_data.items():
            if not current or current_lower in key.lower() or current_lower in title.lower() or current_lower in str(code):
                items.append(app_commands.Choice(name=f"{key} » {title} ({code})", value=key))
                if len(items) >= 25:
                    break
        return items

    @commands.hybrid_command(name="errorcode", description="Look up an idevice error code by name or number")
    @app_commands.describe(name="Start typing to search all error names and codes")
    @app_commands.autocomplete(name=errorcode_autocomplete)
    async def errorcode(self, context: Context, name: str):
        key = name
        if key not in self.key_to_data:
            try:
                num = int(name)
                key = self.code_to_key.get(num)
            except ValueError:
                key = None
        if key is None or key not in self.key_to_data:
            if context.interaction:
                await context.interaction.response.send_message("Error not found.", ephemeral=True)
            else:
                await context.send("Error not found.")
            return
            
        title, code = self.key_to_data[key]
        
        embed = discord.Embed(
            description=f"## Error Code: {code}\n\n**Name**: `{key}`\n**Description**: {title}",
            color=0xfa8c4a,
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Edit Command",
            style=discord.ButtonStyle.secondary,
            url="https://github.com/neoarz/Syntrel/blob/main/cogs/idevice/error_codes.py",
            emoji="<:githubicon:1417717356846776340>"
        ))
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view)
        else:
            await context.send(embed=embed, view=view)

async def setup(bot) -> None:
    cog = ErrorCodes(bot)
    await bot.add_cog(cog)


