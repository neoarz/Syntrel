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
            )
        ]
        super().__init__(placeholder="Choose a SideStore command...", options=options)

    async def callback(self, interaction: discord.Interaction):
        command_name = self.values[0]
        command = self.bot.get_command(command_name)
        
        if command:
            ctx = await self.bot.get_context(interaction.message)
            if ctx:
                await ctx.invoke(command)
                embed = discord.Embed(
                    title="Command Executed",
                    description=f"Successfully executed `/{command_name}`",
                    color=0x00FF00
                )
                embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="Error",
                description="Command not found!",
                color=0xFF0000
            )
            embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
            await interaction.response.edit_message(embed=embed, view=None)


class SidestoreView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(SidestoreSelect(bot))


class Sidestore(commands.Cog, name="sidestore"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="sidestore", description="SideStore troubleshooting and help"
    )
    async def sidestore(self, context: Context) -> None:
        embed = discord.Embed(
            title="SideStore Commands",
            description="Choose a command from the dropdown below to get help with specific issues:",
            color=0x8e82f9
        )
        embed.set_author(name="SideStore", icon_url="https://github.com/SideStore/assets/blob/main/icons/classic/Default.png?raw=true")
        
        view = SidestoreView(self.bot)
        
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await context.send(embed=embed, view=view)


async def setup(bot) -> None:
    await bot.add_cog(Sidestore(bot))
