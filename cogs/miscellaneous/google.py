from urllib.parse import urlencode

from discord.ext import commands


def google_command():
    @commands.hybrid_command(
        name="google",
        description="Open Google or search for a query.",
    )
    async def google(self, context, *, query: str | None = None):
        if query:
            search_url = "https://www.google.com/search?" + urlencode({"q": query})
            message = f"Refer to this magical site for an answer: {search_url}"
        else:
            message = "Refer to this magical site for an answer: https://www.google.com"

        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(message)
            else:
                await inter.followup.send(message)
        else:
            await context.send(message)

    return google
