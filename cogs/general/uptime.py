import discord
from discord.ext import commands

class UptimeView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @discord.ui.button(emoji="<:RefreshEmoji:1418934990770802891>", style=discord.ButtonStyle.primary)
    async def refresh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"The bot has been running for {self.bot.get_uptime()}",
            color=0x7289DA,
        )
        embed.set_author(name="Uptime", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        await interaction.response.edit_message(embed=embed, view=self)

def uptime_command():
    @commands.hybrid_command(
        name="uptime",
        description="Check how long the bot has been running.",
    )
    async def uptime(self, context):
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"The bot has been running for **{self.bot.get_uptime()}**",
            color=0x7289DA,
        )
        embed.set_author(name="Uptime", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        view = UptimeView(self.bot)
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, view=view, ephemeral=True)
            else:
                await inter.followup.send(embed=embed, view=view, ephemeral=True)
        else:
            await context.send(embed=embed, view=view)
    
    return uptime
