import discord
from discord.ext import commands

def ping_command():
    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context):
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x7289DA,
        )
        embed.set_author(name="Ping", icon_url="https://yes.nighty.works/raw/gSxqzV.png")
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=False)
        else:
            await context.send(embed=embed)
    
    return ping
