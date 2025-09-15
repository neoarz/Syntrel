import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Help(commands.Cog, name="help"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def category_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        categories = ["general", "fun", "moderation", "template"]
        
        if await self.bot.is_owner(interaction.user):
            categories.append("owner")
        
        suggestions = []
        for category in categories:
            if current.lower() in category.lower():
                suggestions.append(
                    app_commands.Choice(
                        name=f"{category.capitalize()} Commands",
                        value=category
                    )
                )
        
        return suggestions[:25]

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    @app_commands.describe(category="Choose a specific category to view its commands")
    @app_commands.autocomplete(category=category_autocomplete)
    async def help(self, context: Context, category: str = None) -> None:
        
        category_mapping = {
            "help": "general",
            "botinfo": "general", 
            "serverinfo": "general",
            "ping": "general",
            "invite": "general",
            "server": "general",
            "feedback": "general",
        #   "context_menus": "general",
            
            "randomfact": "fun",
            "coinflip": "fun", 
            "rps": "fun",
            "8ball": "fun",
            
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
                color=0x7289DA
            )
            embed.set_author(name="Help", icon_url="https://yes.nighty.works/raw/T9mnBO.png")
            
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
            
            if context.interaction:
                await context.interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await context.author.send(embed=embed)
            return
        
        category = category.lower()
        if category not in category_descriptions:
            embed = discord.Embed(
                title="Error",
                description=f"Category '{category}' not found. Use `/help` to see available categories.",
                color=0x7289DA
            )
            if context.interaction:
                await context.interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await context.author.send(embed=embed)
            return
        
        if category == "owner" and not (await self.bot.is_owner(context.author)):
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to view owner commands.",
                color=0x7289DA
            )
            if context.interaction:
                await context.interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await context.author.send(embed=embed)
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
                color=0x7289DA
            )
            if context.interaction:
                await context.interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await context.author.send(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"/help » {category.lower()}",
            color=0x7289DA
        )
        embed.set_author(name="Help", icon_url="https://yes.nighty.works/raw/T9mnBO.png")
        data = []
        for command_name, description in sorted(commands_in_category):
            data.append(f"**/{command_name}** » {description}")
        help_text = "\n".join(data)
        embed.add_field(
            name="", 
            value=help_text, 
            inline=False
        )
        if context.interaction:
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.author.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Help(bot))