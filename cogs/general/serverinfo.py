import discord
from discord.ext import commands

def serverinfo_command():
    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @commands.guild_only()
    async def serverinfo(self, context):
        if context.guild is None:
            await context.send("This command can only be used in a server, not in DMs!")
            return
            
        roles = [role.name for role in context.guild.roles]
        num_roles = len(roles)
        if num_roles > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying [50/{num_roles}] Roles")
        roles = ", ".join(roles)
        
        embed = discord.Embed(
            title="**Server Name:**", 
            description=f"{context.guild}", 
            color=0x7289DA
        ).set_author(name="Server Information", icon_url="https://yes.nighty.works/raw/gSxqzV.png")
        
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
            
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", 
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})", 
            value=roles
        )
        embed.set_footer(text=f"Created at: {context.guild.created_at.strftime('%m/%d/%Y')}")
        
        if getattr(context, "interaction", None):
            await context.interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return serverinfo