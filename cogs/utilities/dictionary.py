import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp


def dictionary_command():

    async def send_embed(context, embed: discord.Embed, *, ephemeral: bool = False) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await context.send(embed=embed)

    async def fetch_definition(word: str) -> dict:
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"success": True, "data": data}
                    elif response.status == 404:
                        return {"success": False, "error": "Word not found"}
                    else:
                        return {"success": False, "error": f"API returned status code {response.status}"}
        except aiohttp.ClientError:
            return {"success": False, "error": "Network error occurred"}
        except Exception as e:
            return {"success": False, "error": "An unexpected error occurred"}

    @commands.hybrid_command(
        name="dictionary",
        description="Get the definition of a word",
    )
    @app_commands.describe(
        word="The word to look up"
    )
    async def dictionary(self, context, word: str = None):
        if not word or not word.strip():
            if context.message and context.message.reference and context.message.reference.resolved:
                replied_message = context.message.reference.resolved
                if hasattr(replied_message, 'content') and replied_message.content:
                    word = replied_message.content.strip().split()[0]
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="The replied message has no text content to look up.",
                        color=0xE02B2B,
                    ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                    await send_embed(context, embed, ephemeral=True)
                    return
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Please provide a word to look up or reply to a message with a word.",
                    color=0xE02B2B,
                ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                await send_embed(context, embed, ephemeral=True)
                return
        
        word = word.strip().split()[0]
        
        interaction = getattr(context, "interaction", None)
        if interaction is not None and not interaction.response.is_done():
            await interaction.response.defer()
        
        result = await fetch_definition(word)
        
        if not result["success"]:
            error_message = result.get("error", "Unknown error")
            
            if error_message == "Word not found":
                description = f"Could not find a definition for **{word}**.\nPlease check the spelling and try again."
            else:
                description = f"Failed to fetch definition: {error_message}"
            
            embed = discord.Embed(
                title="Error",
                description=description,
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        data = result["data"]
        
        if not data or len(data) == 0:
            embed = discord.Embed(
                title="Error",
                description=f"No definition found for **{word}**.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        entry = data[0]
        word_title = entry.get("word", word)
        phonetic = entry.get("phonetic", "")
        origin = entry.get("origin", "")
        meanings = entry.get("meanings", [])
        
        embed = discord.Embed(
            title=f"Dictionary",
            description=f"**```{word_title}```**",
            color=0x7289DA,
        )
        embed.set_author(name="Utilities", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
        
        if phonetic:
            embed.add_field(name="Pronunciation", value=f"`{phonetic}`", inline=False)
        
        max_meanings = 3
        for idx, meaning in enumerate(meanings[:max_meanings]):
            part_of_speech = meaning.get("partOfSpeech", "").capitalize()
            definitions = meaning.get("definitions", [])
            
            if definitions:
                def_text = ""
                examples = []
                
                for def_idx, definition in enumerate(definitions[:2], 1):
                    def_line = definition.get("definition", "")
                    example = definition.get("example", "")
                    
                    if def_line:
                        def_text += f"{def_idx}. {def_line}\n"
                        if example:
                            examples.append(f"{def_idx}. {example}")
                
                if def_text:
                    field_name = f"{part_of_speech}" if part_of_speech else f"Definition {idx + 1}"
                    embed.add_field(name=field_name, value=def_text.strip(), inline=False)
                    
                    if examples:
                        example_text = "\n".join(examples)
                        embed.add_field(name="Examples", value=example_text, inline=False)
                        
                        if idx < len(meanings[:max_meanings]) - 1:
                            embed.add_field(name="────────", value="", inline=False)
        
        if origin and len(origin) < 1000:
            embed.add_field(name="Origin", value=origin, inline=False)
        
        synonyms = []
        antonyms = []
        
        for meaning in meanings:
            for definition in meaning.get("definitions", []):
                synonyms.extend(definition.get("synonyms", []))
                antonyms.extend(definition.get("antonyms", []))
        
        if synonyms:
            synonym_text = ", ".join(synonyms[:10])
            embed.add_field(name="Synonyms", value=synonym_text, inline=True)
        
        if antonyms:
            antonym_text = ", ".join(antonyms[:10])
            embed.add_field(name="Antonyms", value=antonym_text, inline=True)

        
        await send_embed(context, embed)

    return dictionary
