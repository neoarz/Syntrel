import discord
from discord.ext import commands


def google_command():
    @commands.hybrid_command(
        name="google",
        description="Search it using this handy dandy tool!",
    )
    async def google(self, context):
        message = "https://google.com"

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(message)
            else:
                await inter.followup.send(message)
        else:
            await context.send(message)

    return google
