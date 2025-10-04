import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class MelonxSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Transfer",
                value="transfer",
                description="How to transfer save files from other emulators or platforms",
            ),
            discord.SelectOption(
                label="Mods",
                value="mods",
                description="How to install mods within MeloNX (Limited Support)",
            ),
            discord.SelectOption(
                label="Game Crash",
                value="gamecrash",
                description="Why does my game crash?",
            ),
            discord.SelectOption(
                label="Requirements",
                value="requirements",
                description="What does MeloNX require?",
            ),
            discord.SelectOption(
                label="Error",
                value="error",
                description="What does this error message mean?",
            ),
            discord.SelectOption(
                label="iOS 26",
                value="26",
                description="How can I run MeloNX on iOS 26?",
            ),
        ]
        super().__init__(placeholder="Choose a MeloNX command...", options=options)

    async def callback(self, interaction: discord.Interaction):
        command_name = self.values[0]
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
                    embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
                    await interaction.response.edit_message(embed=embed, view=None)
            except discord.Forbidden:
                self.bot.logger.warning(f"Bot missing permissions in server {interaction.guild.name} (ID: {interaction.guild.id}) - cannot execute {command_name} command")
                embed = discord.Embed(
                    title="Permission Error",
                    description="The bot doesn't have the required permissions in this server to execute this command. Use the slash command `/{command_name}` instead.",
                    color=0x963155
                )
                embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                self.bot.logger.error(f"Error executing {command_name} command: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while executing the command.",
                    color=0x963155
                )
                embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error",
                description="Command not found!",
                color=0x963155
            )
            embed.set_author(name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png")
            await interaction.response.edit_message(embed=embed, view=None)


class MelonxView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(MelonxSelect(bot))
