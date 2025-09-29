import random
from discord.ext import commands

def eightball_command():
    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    async def eight_ball(self, context, *, question: str):
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = discord.Embed(
            title="8 Ball",
            description=f"{random.choice(answers)}",
            color=0x7289DA,
        )
        embed.set_author(name="Fun", icon_url="https://yes.nighty.works/raw/eW5lLm.webp")
        embed.set_footer(text=f"The question was: {question}")
        await context.send(embed=embed)
    
    return eight_ball
