import discord
from discord.ext import commands
import random
import colorsys

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="color", description="Get a random color.")
    async def color(self, ctx: commands.Context):
        """
        Generates a random color and displays information about it.
        """
        random_color_int = random.randint(0, 0xFFFFFF)
        color = discord.Color(random_color_int)

        r, g, b = color.r, color.g, color.b
        
        # RGB Decimal
        rgb_decimal = (r / 255, g / 255, b / 255)
        
        # HSL and HSV
        h, l, s = colorsys.rgb_to_hls(rgb_decimal[0], rgb_decimal[1], rgb_decimal[2])
        h_hsv, s_hsv, v_hsv = colorsys.rgb_to_hsv(rgb_decimal[0], rgb_decimal[1], rgb_decimal[2])

        embed = discord.Embed(title="Random Color", color=color)
        
        embed.add_field(name="Hex", value=str(color))
        embed.add_field(name="RGB", value=f"rgb({r}, {g}, {b})")
        embed.add_field(name="RGB Decimal", value=f"{rgb_decimal[0]:.3f}, {rgb_decimal[1]:.3f}, {rgb_decimal[2]:.3f}")
        
        embed.add_field(name="HSL", value=f"hsl({h*360:.0f}, {s*100:.0f}%, {l*100:.0f}%)")
        embed.add_field(name="HSV", value=f"hsv({h_hsv*360:.0f}, {s_hsv*100:.0f}%, {v_hsv*100:.0f}%)")
        embed.add_field(name="Integer", value=str(random_color_int))

        # Set the thumbnail to a solid color image using singlecolorimage.com
        embed.set_thumbnail(url=f"https://singlecolorimage.com/get/{str(color).replace('#', '')}/150x150")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))