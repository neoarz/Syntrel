import discord


class LivecontainerSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="26JIT",
                value="26jit",
                description="26JIT information",
            ),
        ]
        super().__init__(placeholder="Choose a LiveContainer command...", options=options)

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
                        name="LiveContainer",
                        icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png",
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
                    name="LiveContainer",
                    icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png",
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
                    name="LiveContainer",
                    icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png",
                )
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error", description="Command not found!", color=0xFF0000
            )
            embed.set_author(
                name="LiveContainer",
                icon_url="https://raw.githubusercontent.com/LiveContainer/LiveContainer/main/screenshots/livecontainer_icon.png",
            )
            await interaction.response.edit_message(embed=embed, view=None)


class LivecontainerView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(LivecontainerSelect(bot))
