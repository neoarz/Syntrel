import discord
from discord.ext import commands


def support_command_idevice():
    @commands.hybrid_command(
        name="support",
        description="Shows proper channels to go to for support in idevice.",
    )
    async def support(self, context):
        message = "For support related to StikDebug or iloader, go to https://discord.com/channels/1329314147434758175/1361741417331953805 or https://discord.com/channels/1329314147434758175/1446681696735989982. Do **NOT** ask for support in general."
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(message)
            else:
                await inter.followup.send(message)
        else:
            await context.send(message)

    return support