import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import json
import os
import math


def load_error_codes():
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'errorcodes.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


class ErrorCodesBrowserView(discord.ui.View):
    def __init__(self, items_per_page=9):
        super().__init__(timeout=300)
        self.error_codes = load_error_codes()
        self.items_per_page = items_per_page
        self.current_page = 0
        self.max_pages = math.ceil(len(self.error_codes) / items_per_page) if self.error_codes else 1
        self.update_buttons()
    
    def update_buttons(self):
        self.clear_items()
        
        first_button = discord.ui.Button(
            emoji="<:leftmax:1420240325770870905>",
            style=discord.ButtonStyle.primary,
            disabled=(self.current_page == 0)
        )
        first_button.callback = self.first_page
        self.add_item(first_button)
        
        prev_button = discord.ui.Button(
            emoji="<:left:1420240344926126090>",
            style=discord.ButtonStyle.primary,
            disabled=(self.current_page == 0)
        )
        prev_button.callback = self.prev_page
        self.add_item(prev_button)
        
        stop_button = discord.ui.Button(
            emoji="<:middle:1420240356087173160>",
            style=discord.ButtonStyle.secondary
        )
        stop_button.callback = self.stop_interaction
        self.add_item(stop_button)
        
        next_button = discord.ui.Button(
            emoji="<:right:1420240334100627456>",
            style=discord.ButtonStyle.primary,
            disabled=(self.current_page >= self.max_pages - 1)
        )
        next_button.callback = self.next_page
        self.add_item(next_button)
        
        last_button = discord.ui.Button(
            emoji="<:rightmax:1420240368846372886>",
            style=discord.ButtonStyle.primary,
            disabled=(self.current_page >= self.max_pages - 1)
        )
        last_button.callback = self.last_page
        self.add_item(last_button)
    
    def create_embed(self):
        if not self.error_codes:
            embed = discord.Embed(
                title="Error Codes",
                description="No error codes found.",
                color=0xfa8c4a
            )
            embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
            embed.set_footer(text="Page 0 of 0")
            return embed
        
        embed = discord.Embed(
            title="Error Codes",
            color=0xfa8c4a
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.error_codes))
        current_codes = self.error_codes[start_idx:end_idx]
        
        for i, error in enumerate(current_codes):
            field_value = f"**Code:** `{error.get('code', 'N/A')}`\n**Name:** `{error.get('name', 'Unknown')}`\n**Description:** {error.get('description', 'No description')}"
            embed.add_field(
                name="\u200b",
                value=field_value,
                inline=True
            )
        

        while len(current_codes) % 3 != 0:
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        
        embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_pages}")
        
        return embed
    
    async def first_page(self, interaction: discord.Interaction):
        self.current_page = 0
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def prev_page(self, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def stop_interaction(self, interaction: discord.Interaction):
        self.clear_items()
        embed = self.create_embed()
        embed.set_footer(text="Interaction stopped")
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()
    
    async def next_page(self, interaction: discord.Interaction):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def last_page(self, interaction: discord.Interaction):
        self.current_page = self.max_pages - 1
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)


class ideviceSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="No Apps",
                value="noapps",
                description="Help when apps aren't showing in installed apps view",
            ),
            discord.SelectOption(
                label="Error Codes",
                value="errorcodes",
                description="Browse idevice error codes",
            ),
        ]
        super().__init__(placeholder="Choose an idevice command...", options=options)

    async def callback(self, interaction: discord.Interaction):
        command_name = self.values[0]

        if command_name == "errorcodes":
            try:
                view = ErrorCodesBrowserView()
                embed = view.create_embed()
                
                success_embed = discord.Embed(
                    title="Command Executed",
                    description="Successfully executed `/errorcodes`. Please run /[errorcode_name] to get more information about an error code, and send it in chat",
                    color=0x00FF00
                )
                success_embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=success_embed, view=None)
                
                await interaction.followup.send(embed=embed, view=view, ephemeral=True)
                
            except discord.Forbidden:
                self.bot.logger.warning(f"Bot missing permissions in server {interaction.guild.name} (ID: {interaction.guild.id}) - cannot execute errorcodes command")
                embed = discord.Embed(
                    title="Permission Error",
                    description="The bot doesn't have the required permissions in this server to execute this command. Use the slash command `/errorcodes` instead.",
                    color=0xFF0000
                )
                embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                self.bot.logger.error(f"Error executing errorcodes command: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while executing the command.",
                    color=0xFF0000
                )
                embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=embed, view=None)
            return
        
        command = self.bot.get_command(command_name)
        
        if command:
            try:
                ctx = await self.bot.get_context(interaction.message)
                if ctx:
                    await ctx.invoke(command)
                    embed = discord.Embed(
                        title="Command Executed",
                        description=f"Successfully executed `/{command_name}`",
                        color=0x00FF00
                    )
                    embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                    await interaction.response.edit_message(embed=embed, view=None)
            except discord.Forbidden:
                self.bot.logger.warning(f"Bot missing permissions in server {interaction.guild.name} (ID: {interaction.guild.id}) - cannot execute {command_name} command")
                embed = discord.Embed(
                    title="Permission Error",
                    description=f"The bot doesn't have the required permissions in this server to execute this command. Use the slash command `/{command_name}` instead.",
                    color=0xFF0000
                )
                embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                self.bot.logger.error(f"Error executing {command_name} command: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while executing the command.",
                    color=0xFF0000
                )
                embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error",
                description="Command not found!",
                color=0xFF0000
            )
            embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
            await interaction.response.edit_message(embed=embed, view=None)


class ideviceView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(ideviceSelect(bot))


class idevice(commands.Cog, name="idevice"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="idevice", description="idevice troubleshooting and help"
    )
    async def idevice(self, context: Context) -> None:
        embed = discord.Embed(
            title="idevice Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0xfa8c4a
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        
        view = ideviceView(self.bot)
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(idevice(bot))