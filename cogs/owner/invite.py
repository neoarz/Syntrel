import os
import discord
from discord.ext import commands
from discord.ext.commands import Context


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
    @commands.is_owner()
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
        embed = discord.Embed(title="Invite", description=f"Invite me by clicking [here]({invite_url}).", color=0x7289DA)
        embed.set_author(name="Owner", icon_url="https://yes.nighty.works/raw/zReOib.webp")
        
        try:
            await context.author.send(embed=embed)
            await self.send_embed(context, discord.Embed(description="I sent you a private message!", color=0x7289DA), ephemeral=True)
        except discord.Forbidden:
            await self.send_embed(context, embed, ephemeral=True)

    async def cog_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.NotOwner):
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
