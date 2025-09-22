import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class IdeviceSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="No Apps",
                value="noapps",
                description="Help when apps aren't showing in installed apps view",
            )
        ]
        super().__init__(placeholder="Choose an iDevice command...", options=options)

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
                    embed.set_author(name="iDevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                    await interaction.response.edit_message(embed=embed, view=None)
            except discord.Forbidden:
                self.bot.logger.warning(f"Bot missing permissions in server {interaction.guild.name} (ID: {interaction.guild.id}) - cannot execute {command_name} command")
                embed = discord.Embed(
                    title="Permission Error",
                    description="The bot doesn't have the required permissions in this server to execute commands. Please contact a server administrator to add the bot to the server.",
                    color=0xFF0000
                )
                embed.set_author(name="iDevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                self.bot.logger.error(f"Error executing {command_name} command: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while executing the command.",
                    color=0xFF0000
                )
                embed.set_author(name="iDevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error",
                description="Command not found!",
                color=0xFF0000
            )
            embed.set_author(name="iDevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
            await interaction.response.edit_message(embed=embed, view=None)


class IdeviceView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(IdeviceSelect(bot))


class Idevice(commands.Cog, name="idevice"):
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
        
        view = IdeviceView(self.bot)
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Idevice(bot))
