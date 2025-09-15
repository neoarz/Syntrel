# This is not used anymore, but I'm keeping it here for reference
# TODO: Remove this once we have a better way to handle context menus

# import discord
# from discord import app_commands
# from discord.ext import commands
#
#
# class ContextMenus(commands.Cog, name="context_menus"):
#     def __init__(self, bot) -> None:
#         self.bot = bot
#         self.context_menu_user = app_commands.ContextMenu(
#             name="Grab ID", callback=self.grab_id
#         )
#         self.bot.tree.add_command(self.context_menu_user)
#         self.context_menu_message = app_commands.ContextMenu(
#             name="Remove spoilers", callback=self.remove_spoilers
#         )
#         self.bot.tree.add_command(self.context_menu_message)
#
#     async def remove_spoilers(
#         self, interaction: discord.Interaction, message: discord.Message
#     ) -> None:
#         """
#         Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.
#
#         :param interaction: The application command interaction.
#         :param message: The message that is being interacted with.
#         """
#         spoiler_attachment = None
#         for attachment in message.attachments:
#             if attachment.is_spoiler():
#                 spoiler_attachment = attachment
#                 break
#         embed = discord.Embed(
#             title="Message without spoilers",
#             description=message.content.replace("||", ""),
#             color=0xBEBEFE,
#         )
#         if spoiler_attachment is not None:
#             embed.set_image(url=attachment.url)
#         await interaction.response.send_message(embed=embed, ephemeral=True)
#
#     async def grab_id(
#         self, interaction: discord.Interaction, user: discord.User
#     ) -> None:
#         """
#         Grabs the ID of the user.
#
#         :param interaction: The application command interaction.
#         :param user: The user that is being interacted with.
#         """
#         embed = discord.Embed(
#             description=f"The ID of {user.mention} is `{user.id}`.",
#             color=0xBEBEFE,
#         )
#         await interaction.response.send_message(embed=embed, ephemeral=True)
#
#
# async def setup(bot) -> None:
#     await bot.add_cog(ContextMenus(bot))
