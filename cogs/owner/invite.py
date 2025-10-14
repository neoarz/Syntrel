import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils.checks import is_owner_or_friend


class Invite(commands.Cog, name="invite"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def send_embed(self, context: Context, embed: discord.Embed, *, ephemeral: bool = False) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @is_owner_or_friend()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        client = self.bot.user
        if client is None:
            await context.send("Bot is not ready. Try again shortly.")
            return
        invite_link = os.getenv("INVITE_LINK")
        embed = discord.Embed(title="Install", description=f"Install me by clicking [here]({invite_link}).", color=0x7289DA)
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        
        await self.send_embed(context, embed, ephemeral=False)

    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, (commands.NotOwner, commands.CheckFailure)):
            embed = discord.Embed(
                title="Permission Denied",
                description="You are not the owner of this bot.",
                color=0xE02B2B
            )
            embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
            await self.send_embed(context, embed, ephemeral=True)
        else:
            raise error


async def setup(bot) -> None:
    await bot.add_cog(Invite(bot))
