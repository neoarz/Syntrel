import discord
from discord import Interaction, ButtonStyle, SelectOption
from discord.ui import Modal, TextInput, View, Button, Select
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .models import Tag, TagButton

class TagEmbed(discord.Embed):
    def __init__(self, tag: "Tag", author_name: str):
        super().__init__(
            description=tag.content,
            color=0x7289DA,
            timestamp=discord.utils.utcnow()
        )
        self.set_author(name="Tags", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
        self.set_footer(text=f"Created by {author_name} | Used {tag.used} times")


class TagButtonView(View):
    def __init__(self, buttons: List["TagButton"]):
        super().__init__(timeout=None)
        for button in buttons[:5]:
            self.add_item(TagUrlButton(button))


class TagUrlButton(Button):
    def __init__(self, tag_button: "TagButton"):
        super().__init__(
            label=tag_button.label,
            url=tag_button.url,
            emoji=tag_button.emoji,
            style=ButtonStyle.link
        )


class CreateTagModal(Modal):
    def __init__(self, cog):
        super().__init__(title="Create New Tag")
        self.cog = cog

        self.name_input = TextInput(
            label="Tag Name",
            placeholder="Enter the name for your tag...",
            max_length=100,
            required=True
        )
        self.content_input = TextInput(
            label="Tag Content",
            placeholder="Enter the content for your tag...",
            style=discord.TextStyle.paragraph,
            max_length=2000,
            required=True
        )

        self.add_item(self.name_input)
        self.add_item(self.content_input)

    async def on_submit(self, interaction: Interaction):
        name = self.name_input.value
        content = self.content_input.value
        author = interaction.user.id
        guild = interaction.guild.id if interaction.guild else None

        existing_tag = await self.cog.conn.tag(name=name)
        if existing_tag and (existing_tag.guild == guild or existing_tag.guild is None):
            await interaction.response.send_message(
                f"A tag with the name '{name}' already exists!",
                ephemeral=True
            )
            return

        try:
            tag = await self.cog.conn.create_tag(name, content, author, guild)
            embed = discord.Embed(
                title="Tag Created!",
                description=f"Successfully created tag `{name}`!",
                color=0x7289DA
            )
            embed.set_author(name="Tags", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            self.cog.logger.info(f"Tag '{name}' created by {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while creating the tag: {str(e)}",
                ephemeral=True
            )


class EditTagPreview(View):
    def __init__(self, cog, tag: "Tag"):
        super().__init__(timeout=300)
        self.cog = cog
        self.tag = tag

    @discord.ui.button(label="Edit", style=ButtonStyle.primary)
    async def edit_button(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.tag.author and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You don't have permission to edit this tag!",
                ephemeral=True
            )
            return
        await interaction.response.send_modal(EditTagModal(self.cog, self.tag))

    @discord.ui.button(label="Close", style=ButtonStyle.danger)
    async def close_button(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(content="Tag edit cancelled.", embed=None, view=None)


class EditTagModal(Modal):
    def __init__(self, cog, tag: "Tag"):
        super().__init__(title=f"Edit Tag: {tag.name}")
        self.cog = cog
        self.tag = tag

        self.name_input = TextInput(
            label="Tag Name",
            default=tag.name,
            max_length=100,
            required=True
        )
        self.content_input = TextInput(
            label="Tag Content",
            default=tag.content,
            style=discord.TextStyle.paragraph,
            max_length=2000,
            required=True
        )

        self.add_item(self.name_input)
        self.add_item(self.content_input)

    async def on_submit(self, interaction: Interaction):
        if interaction.user.id != self.tag.author and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You don't have permission to edit this tag!",
                ephemeral=True
            )
            return

        name = self.name_input.value
        content = self.content_input.value

        guild = interaction.guild.id if interaction.guild else None
        existing_tag = await self.cog.conn.tag(name=name)
        if existing_tag and existing_tag.tid != self.tag.tid and (existing_tag.guild == guild or existing_tag.guild is None):
            await interaction.response.send_message(
                f"A tag with the name '{name}' already exists!",
                ephemeral=True
            )
            return

        try:
            self.tag.name = name
            self.tag.content = content
            await self.cog.conn.update(self.tag)
            embed = discord.Embed(
                title="Success!",
                description=f"Successfully updated tag `{name}`!",
                color=0x00FF00
            )
            embed.set_author(name="Tags", icon_url="https://yes.nighty.works/raw/y5SEZ9.webp")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            self.cog.logger.info(f"Tag '{name}' updated by {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while updating the tag: {str(e)}",
                ephemeral=True
            )


class ConfirmDeleteTag(View):
    def __init__(self, cog, tag: "Tag"):
        super().__init__(timeout=60)
        self.cog = cog
        self.tag = tag

    @discord.ui.button(label="Yes", style=ButtonStyle.danger)
    async def confirm_delete(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.tag.author and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You don't have permission to delete this tag!",
                ephemeral=True
            )
            return

        try:
            await self.cog.conn.delete_tag(self.tag)
            await interaction.response.edit_message(
                embed=discord.Embed(
                    title="Success!",
                    description=f"Tag `{self.tag.name}` has been deleted.",
                    color=0x00FF00
                ),
                view=None
            )
            self.cog.logger.info(f"Tag '{self.tag.name}' deleted by {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while deleting the tag: {str(e)}",
                ephemeral=True
            )

    @discord.ui.button(label="No", style=ButtonStyle.secondary)
    async def cancel_delete(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content="Tag deletion cancelled.",
            view=None
        )


class AddTagButtonModal(Modal):
    def __init__(self, cog, tag: "Tag"):
        super().__init__(title=f"Add Button to: {tag.name}")
        self.cog = cog
        self.tag = tag

        self.label_input = TextInput(
            label="Button Label",
            placeholder="Enter the button label...",
            max_length=80,
            required=True
        )
        self.url_input = TextInput(
            label="Button URL",
            placeholder="https://example.com",
            max_length=512,
            required=True
        )
        self.emoji_input = TextInput(
            label="Button Emoji (Optional)",
            placeholder="Enter emoji...",
            max_length=100,
            required=False
        )

        self.add_item(self.label_input)
        self.add_item(self.url_input)
        self.add_item(self.emoji_input)

    async def on_submit(self, interaction: Interaction):
        if interaction.user.id != self.tag.author and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You don't have permission to modify this tag!",
                ephemeral=True
            )
            return

        if len(self.tag.buttons) >= 5:
            await interaction.response.send_message(
                "Tags can only have up to 5 buttons!",
                ephemeral=True
            )
            return

        label = self.label_input.value
        url = self.url_input.value
        emoji = self.emoji_input.value if self.emoji_input.value else None

        try:
            await self.cog.conn.add_button(self.tag, label, url, emoji)
            await interaction.response.send_message(
                f"Successfully added button '{label}' to tag '{self.tag.name}'!",
                ephemeral=True
            )
            self.cog.logger.info(f"Button '{label}' added to tag '{self.tag.name}' by {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while adding the button: {str(e)}",
                ephemeral=True
            )


class TagSelectButton(Select):
    def __init__(self, cog, tag: "Tag", delete_mode: bool = False, safe: bool = False):
        self.cog = cog
        self.tag = tag
        self.delete_mode = delete_mode
        
        options = []
        for i, button in enumerate(tag.buttons[:25]):
            option_label = button.label
            if len(option_label) > 100:
                option_label = option_label[:97] + "..."
            
            options.append(SelectOption(
                label=option_label,
                value=str(button.id),
                description=button.url[:100] if len(button.url) <= 100 else button.url[:97] + "...",
                emoji=button.emoji if not safe else None
            ))

        if not options:
            options.append(SelectOption(
                label="No buttons available",
                value="none",
                description="This tag has no buttons"
            ))

        super().__init__(
            placeholder="Select a button to edit..." if not delete_mode else "Select a button to delete...",
            options=options,
            disabled=len(tag.buttons) == 0
        )

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.tag.author and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You don't have permission to modify this tag!",
                ephemeral=True
            )
            return

        if self.values[0] == "none":
            await interaction.response.send_message(
                "No buttons available to modify.",
                ephemeral=True
            )
            return

        button_id = int(self.values[0])
        button = next((b for b in self.tag.buttons if b.id == button_id), None)
        
        if not button:
            await interaction.response.send_message(
                "Button not found!",
                ephemeral=True
            )
            return

        if self.delete_mode:
            try:
                await self.cog.conn.delete_button(button)
                await interaction.response.send_message(
                    f"Successfully deleted button '{button.label}' from tag '{self.tag.name}'!",
                    ephemeral=True
                )
                self.cog.logger.info(f"Button '{button.label}' deleted from tag '{self.tag.name}' by {interaction.user.name}")
            except Exception as e:
                await interaction.response.send_message(
                    f"An error occurred while deleting the button: {str(e)}",
                    ephemeral=True
                )
        else:
            await interaction.response.send_modal(EditTagButtonModal(self.cog, self.tag, button))


class EditTagButtonModal(Modal):
    def __init__(self, cog, tag: "Tag", button: "TagButton"):
        super().__init__(title=f"Edit Button: {button.label}")
        self.cog = cog
        self.tag = tag
        self.button = button

        self.label_input = TextInput(
            label="Button Label",
            default=button.label,
            max_length=80,
            required=True
        )
        self.url_input = TextInput(
            label="Button URL",
            default=button.url,
            max_length=512,
            required=True
        )
        self.emoji_input = TextInput(
            label="Button Emoji (Optional)",
            default=button.emoji or "",
            max_length=100,
            required=False
        )

        self.add_item(self.label_input)
        self.add_item(self.url_input)
        self.add_item(self.emoji_input)

    async def on_submit(self, interaction: Interaction):
        label = self.label_input.value
        url = self.url_input.value
        emoji = self.emoji_input.value if self.emoji_input.value else None

        try:
            self.button.label = label
            self.button.url = url
            self.button.emoji = emoji
            await self.cog.conn.update_button(self.button)
            await interaction.response.send_message(
                f"Successfully updated button '{label}' on tag '{self.tag.name}'!",
                ephemeral=True
            )
            self.cog.logger.info(f"Button '{label}' updated on tag '{self.tag.name}' by {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while updating the button: {str(e)}",
                ephemeral=True
            )
