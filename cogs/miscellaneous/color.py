import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import random


def color_command():
    @commands.hybrid_command(
        name="color",
        description="Generate a random color with details",
    )
    async def color(self, context):
        # Generate random color values
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        # Convert to hex
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Calculate HSL
        r_norm, g_norm, b_norm = r/255, g/255, b/255
        max_val = max(r_norm, g_norm, b_norm)
        min_val = min(r_norm, g_norm, b_norm)
        l = (max_val + min_val) / 2
        
        if max_val == min_val:
            h = s = 0
        else:
            d = max_val - min_val
            s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
            
            if max_val == r_norm:
                h = (g_norm - b_norm) / d + (6 if g_norm < b_norm else 0)
            elif max_val == g_norm:
                h = (b_norm - r_norm) / d + 2
            else:
                h = (r_norm - g_norm) / d + 4
            h /= 6
        
        h_deg = int(h * 360)
        s_pct = int(s * 100)
        l_pct = int(l * 100)
        
        # Calculate HSV
        v = max_val
        s_v = 0 if v == 0 else d / max_val
        h_v_deg = h_deg
        s_v_pct = int(s_v * 100)
        v_pct = int(v * 100)
        
        # Calculate integer representation
        integer_val = (r << 16) + (g << 8) + b
        
        # Create embed
        embed = discord.Embed(
            title="Random Color",
            color=int(hex_color[1:], 16)
        )
        embed.set_author(name="Color", icon_url="https://yes.nighty.works/raw/YxMC0r.png")
        
        # Add color information
        embed.add_field(name="Hex", value=hex_color, inline=True)
        embed.add_field(name="RGB", value=f"rgb({r}, {g}, {b})", inline=True)
        embed.add_field(name="RGB Decimal", value=f"{r/255:.3f}, {g/255:.3f}, {b/255:.3f}", inline=True)
        
        embed.add_field(name="HSL", value=f"hsl({h_deg}, {s_pct}%, {l_pct}%)", inline=True)
        embed.add_field(name="HSV", value=f"hsv({h_v_deg}, {s_v_pct}%, {v_pct}%)", inline=True)
        embed.add_field(name="Integer", value=str(integer_val), inline=True)
        
        # Set thumbnail to color image from singlecolorimage.com
        image_url = f"https://singlecolorimage.com/get/{hex_color[1:]}/200x200"
        embed.set_thumbnail(url=image_url)
        
        if getattr(context, "interaction", None):
            inter = context.interaction
            if not inter.response.is_done():
                await inter.response.send_message(embed=embed, ephemeral=False)
            else:
                await inter.followup.send(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    return color