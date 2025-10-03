import platform
import discord
from discord.ext import commands

def botinfo_command():
    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context):
        embed = discord.Embed(
            title="Syntrel Discord Bot",
            color=0x7289DA,
        )
        embed.set_author(name="Bot Information", icon_url="https://yes.nighty.works/raw/gSxqzV.png")
        embed.add_field(name="Owner:", value="[neoarz](https://discordapp.com/users/1015372540937502851)", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.bot_prefix} for normal commands",
            inline=False,
        )
        if getattr(context, "interaction", None):
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return botinfo