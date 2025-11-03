import discord
from discord.ext import commands


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
            discord.SelectOption(
                label="Upgrade",
                value="upgrade",
                description="How can I upgrade my firmware and keys in MeloNX?",
            ),
            discord.SelectOption(
                label="Legal",
                value="legal",
                description="Legality of emulators and our stance on piracy",
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
                        color=0x00FF00,
                    )
                    embed.set_author(
                        name="MeloNX",
                        icon_url="https://yes.nighty.works/raw/TLGaVa.png",
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
                    name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
                )
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                self.bot.logger.error(f"Error executing {command_name} command: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An error occurred while executing the command.",
                    color=0x963155,
                )
                embed.set_author(
                    name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
                )
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error", description="Command not found!", color=0x963155
            )
            embed.set_author(
                name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
            )
            await interaction.response.edit_message(embed=embed, view=None)


class MelonxView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(MelonxSelect(bot))


def melonx_command():
    @commands.hybrid_command(
        name="melonx", description="MeloNX troubleshooting and help"
    )
    async def melonx(self, context):
        if isinstance(context.channel, discord.DMChannel):
            embed = discord.Embed(
                title="Error",
                description="This command can only be used in servers.",
                color=0xE02B2B,
            )
            embed.set_author(
                name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
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
                name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
            )

            if context.interaction:
                await context.interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            else:
                await context.send(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="MeloNX Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x963155,
        )
        embed.set_author(
            name="MeloNX", icon_url="https://yes.nighty.works/raw/TLGaVa.png"
        )

        view = MelonxView(self.bot)

        if context.interaction:
            await context.interaction.response.send_message(
                embed=embed, view=view, ephemeral=True
            )
        else:
            await context.send(embed=embed, view=view)

    return melonx
