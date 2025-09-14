"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.4.0
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Help(commands.Cog, name="help"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    @app_commands.describe(category="Choose a specific category to view its commands")
    async def help(self, context: Context, category: str = None) -> None:
        
        category_mapping = {
            "help": "general",
            "botinfo": "general", 
            "serverinfo": "general",
            "ping": "general",
            "invite": "general",
            "server": "general",
            "8ball": "general",
            "bitcoin": "general",
            "feedback": "general",
            "context_menus": "general",
            
            "randomfact": "fun",
            "coinflip": "fun", 
            "rps": "fun",
            
            "kick": "moderation",
            "ban": "moderation",
            "nick": "moderation",
            "purge": "moderation",
            "hackban": "moderation",
            "warnings": "moderation",
            "archive": "moderation",
            
            "sync": "owner",
            "cog_management": "owner",
            "shutdown": "owner",
            "say": "owner",
            
            "testcommand": "template"
        }
        
        category_descriptions = {
            "general": "General commands",
            "fun": "Funny commands", 
            "moderation": "Administration commands",
            "template": "Template commands",
            "owner": "Owner commands"
        }
        
        if category is None:
            embed = discord.Embed(
                title="Help", 
                color=0xBEBEFE
            )
            
            available_categories = set()
            for cog_name in self.bot.cogs:
                mapped_category = category_mapping.get(cog_name.lower())
                if mapped_category:
                    if mapped_category == "owner" and not (await self.bot.is_owner(context.author)):
                        continue
                    available_categories.add(mapped_category)
            
            category_list = []
            for cat in sorted(available_categories):
                description = category_descriptions.get(cat, f"{cat.capitalize()} commands")
                category_list.append(f"**/help {cat}** » {description}")
            
            if category_list:
                embed.add_field(
                    name="", 
                    value="\n".join(category_list), 
                    inline=False
                )
            
            await context.send(embed=embed)
            return
        
        category = category.lower()
        if category not in category_descriptions:
            embed = discord.Embed(
                title="Error",
                description=f"Category '{category}' not found. Use `/help` to see available categories.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        
        if category == "owner" and not (await self.bot.is_owner(context.author)):
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to view owner commands.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        
        commands_in_category = []
        for cog_name in self.bot.cogs:
            if category_mapping.get(cog_name.lower()) == category:
                cog = self.bot.get_cog(cog_name)
                if cog:
                    commands_list = cog.get_commands()
                    for command in commands_list:
                        description = command.description.partition("\n")[0] if command.description else "No description available"
                        commands_in_category.append((command.name, description))
        
        if not commands_in_category:
            embed = discord.Embed(
                title="Error",
                description=f"No commands found in category '{category}'.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="Help",
            color=0xBEBEFE
        )
        
        data = []
        for command_name, description in sorted(commands_in_category):
            data.append(f"**{command_name}** » {description}")
        
        help_text = "\n".join(data)
        embed.add_field(
            name=f"{category.capitalize()} Commands", 
            value=help_text, 
            inline=False
        )
        
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Help(bot))
