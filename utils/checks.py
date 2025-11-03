import os
from discord.ext import commands


def get_owner_friend_ids():
    owner_friends = os.getenv("OWNER_FRIENDS", "")
    if not owner_friends.strip():
        return []
    return [int(id.strip()) for id in owner_friends.split(",") if id.strip().isdigit()]


def is_owner_or_friend():
    async def predicate(ctx):
        owner_friend_ids = get_owner_friend_ids()
        return ctx.author.id in owner_friend_ids or await ctx.bot.is_owner(ctx.author)

    return commands.check(predicate)
