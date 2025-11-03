import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import time


class SidestoreSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Refresh Issues",
                value="refresh",
                description="Help with refreshing or installing apps",
            ),
            discord.SelectOption(
                label="Verification Code",
                value="code",
                description="No code received when signing in with Apple ID",
            ),
            discord.SelectOption(
                label="App Crashes",
                value="crash",
                description="Help with SideStore crashing issues",
            ),
            discord.SelectOption(
                label="Pairing File",
                value="pairing",
                description="Help with pairing file issues",
            ),
            discord.SelectOption(
                label="Anisette Server",
                value="server",
                description="Help with anisette server issues",
            ),
            discord.SelectOption(
                label="Apps Stuck Halfway",
                value="half",
                description="Help when apps get stuck installing",
            ),
            discord.SelectOption(
                label="SparseRestore",
                value="sparse",
                description="Information about SparseRestore exploit",
            ),
            discord.SelectOption(
                label="AFC Connection Failure",
                value="afc",
                description="Help with AFC Connection Failure issues",
            ),
            discord.SelectOption(
                label="UDID Error",
                value="udid",
                description="SideStore could not determine device UDID",
            ),
        ]
        super().__init__(placeholder="Choose a SideStore command...", options=options)

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
                        color=0x00FF00,
                    )
                    embed.set_author(
                        name="SideStore",
                        icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
                    )
                    await interaction.response.edit_message(embed=embed, view=None)
            except discord.Forbidden:
                guild_info = (
                    f"server {interaction.guild.name} (ID: {interaction.guild.id})"
                    if interaction.guild
                    else "DM or private channel"
                )
                self.bot.logger.warning(
                    f"Bot missing permissions in {guild_info} - cannot execute {command_name} command"
                )

                if interaction.guild is None:
                    embed = discord.Embed(
                        title="Error",
                        description="This command cannot be executed in DMs.",
                        color=0xFF0000,
                    )
                else:
                    embed = discord.Embed(
                        title="Permission Error",
                        description="The bot needs the `send messages` permission to execute this command.",
                        color=0xFF0000,
                    )
                embed.set_author(
                    name="SideStore",
                    icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
                )
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                self.bot.logger.error(f"Error executing {command_name} command: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while executing the command.",
                    color=0xFF0000,
                )
                embed.set_author(
                    name="SideStore",
                    icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
                )
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error", description="Command not found!", color=0xFF0000
            )
            embed.set_author(
                name="SideStore",
                icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
            )
            await interaction.response.edit_message(embed=embed, view=None)


class SidestoreView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(SidestoreSelect(bot))


def sidestore_command():
    @commands.hybrid_command(
        name="help", description="SideStore troubleshooting and help"
    )
    async def sidestore(self, context):
        if isinstance(context.channel, discord.DMChannel):
            embed = discord.Embed(
                title="Error",
                description="This command can only be used in servers.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="SideStore",
                icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
            )

            if context.interaction:
                await context.interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            else:
                await context.send(embed=embed, ephemeral=True)
            return

        if isinstance(context.channel, discord.PartialMessageable):
            embed = discord.Embed(
                title="Error",
                description="The bot needs send messages permissions in this channel.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="SideStore",
                icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
            )

            if context.interaction:
                await context.interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            else:
                await context.send(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="SideStore Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x8E82F9,
        )
        embed.set_author(
            name="SideStore",
            icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true",
        )

        view = SidestoreView(self.bot)

        if context.interaction:
            await context.interaction.response.send_message(
                embed=embed, view=view, ephemeral=True
            )
        else:
            await context.send(embed=embed, view=view)

    return sidestore
