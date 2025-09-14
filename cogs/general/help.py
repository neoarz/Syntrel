"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.4.0
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Help(commands.Cog, name="help"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xBEBEFE
        )
        
        category_mapping = {
            "help": "General",
            "botinfo": "General", 
            "serverinfo": "General",
            "ping": "General",
            "invite": "General",
            "server": "General",
            "8ball": "General",
            "bitcoin": "General",
            "feedback": "General",
            "context_menus": "General",
            
            "randomfact": "Fun",
            "coinflip": "Fun", 
            "rps": "Fun",
            
            "kick": "Moderation",
            "ban": "Moderation",
            "nick": "Moderation",
            "purge": "Moderation",
            "hackban": "Moderation",
            "warnings": "Moderation",
            "archive": "Moderation",
            
            
            "sync": "Owner",
            "cog_management": "Owner",
            "shutdown": "Owner",
            "say": "Owner",
            
        
            "testcommand": "Template"
        }
        
    
        categories = {}
        
        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            if cog:
                commands_list = cog.get_commands()
                for command in commands_list:
                    category = category_mapping.get(cog_name.lower(), "Other")
                    if category == "Owner" and not (await self.bot.is_owner(context.author)):
                        continue
                    
                    if category not in categories:
                        categories[category] = []
                    
                    description = command.description.partition("\n")[0] if command.description else "No description available"
                    categories[category].append((command.name, description))
        
        category_order = ["General", "Fun", "Moderation", "Template", "Owner", "Other"]
        
        for category in category_order:
            if category in categories and categories[category]:
                data = []
                for command_name, description in sorted(categories[category]):
                    data.append(f"{command_name} - {description}")
                help_text = "\n".join(data)
                embed.add_field(
                    name=category, value=f"```{help_text}```", inline=False
                )
        
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Help(bot))
