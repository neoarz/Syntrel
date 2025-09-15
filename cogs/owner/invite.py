import os
import discord
from discord.ext import commands
from discord.ext.commands import Context


class Invite(commands.Cog, name="invite"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        client = self.bot.user
        if client is None:
            await context.send("Bot is not ready. Try again shortly.")
            return
        permissions = os.getenv("INVITE_PERMISSIONS", "0")
        invite_url = (
            f"https://discord.com/api/oauth2/authorize?client_id={client.id}"
            f"&scope=bot%20applications.commands&permissions={permissions}"
        )
        embed = discord.Embed(description=f"Invite me by clicking [here]({invite_url}).", color=0x7289DA)
        embed.set_author(name="Invite Me", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Invite(bot))
