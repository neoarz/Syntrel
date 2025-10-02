import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import asyncio
import re
import json
import urllib.parse


languages = {
            "auto": "Auto-detect",
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
            "ar": "Arabic",
            "hi": "Hindi",
            "th": "Thai",
            "vi": "Vietnamese",
            "nl": "Dutch",
            "pl": "Polish",
            "tr": "Turkish",
            "sv": "Swedish",
            "da": "Danish",
            "no": "Norwegian",
            "fi": "Finnish",
            "cs": "Czech",
            "sk": "Slovak",
            "hu": "Hungarian",
            "ro": "Romanian",
            "bg": "Bulgarian",
            "hr": "Croatian",
            "sr": "Serbian",
            "sl": "Slovenian",
            "et": "Estonian",
            "lv": "Latvian",
            "lt": "Lithuanian",
            "uk": "Ukrainian",
            "be": "Belarusian",
            "mk": "Macedonian",
            "sq": "Albanian",
            "mt": "Maltese",
            "is": "Icelandic",
            "ga": "Irish",
            "cy": "Welsh",
            "gd": "Scots Gaelic",
            "eu": "Basque",
            "ca": "Catalan",
            "gl": "Galician",
            "eo": "Esperanto",
            "la": "Latin",
            "af": "Afrikaans",
            "sw": "Swahili",
            "zu": "Zulu",
            "xh": "Xhosa",
            "yo": "Yoruba",
            "ig": "Igbo",
            "ha": "Hausa",
            "am": "Amharic",
            "om": "Oromo",
            "ti": "Tigrinya",
            "so": "Somali",
            "rw": "Kinyarwanda",
            "lg": "Ganda",
            "ny": "Chichewa",
            "sn": "Shona",
            "st": "Sesotho",
            "tn": "Tswana",
            "ts": "Tsonga",
            "ss": "Swati",
            "nr": "Ndebele",
            "nso": "Northern Sotho",
            "ve": "Venda",
            "bn": "Bengali",
            "gu": "Gujarati",
            "kn": "Kannada",
            "ml": "Malayalam",
            "mr": "Marathi",
            "ne": "Nepali",
            "or": "Odia",
            "pa": "Punjabi",
            "si": "Sinhala",
            "ta": "Tamil",
            "te": "Telugu",
            "ur": "Urdu",
            "as": "Assamese",
            "bho": "Bhojpuri",
            "doi": "Dogri",
            "gom": "Konkani",
            "mai": "Maithili",
            "mni-Mtei": "Meiteilon",
            "sa": "Sanskrit",
            "id": "Indonesian",
            "ms": "Malay",
            "tl": "Filipino",
            "jv": "Javanese",
            "su": "Sundanese",
            "ceb": "Cebuano",
            "hil": "Hiligaynon",
            "ilo": "Iloko",
            "pam": "Kapampangan",
            "war": "Waray",
            "my": "Myanmar",
            "km": "Khmer",
            "lo": "Lao",
            "ka": "Georgian",
            "hy": "Armenian",
            "az": "Azerbaijani",
            "kk": "Kazakh",
            "ky": "Kyrgyz",
            "mn": "Mongolian",
            "tk": "Turkmen",
            "ug": "Uyghur",
            "uz": "Uzbek",
            "tg": "Tajik",
            "fa": "Persian",
            "ps": "Pashto",
            "sd": "Sindhi",
            "he": "Hebrew",
            "yi": "Yiddish",
            "iw": "Hebrew",
            "el": "Greek",
            "lt": "Lithuanian",
            "lv": "Latvian",
        }

async def language_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    current = current.lower()
    choices = []
    
    for code, name in languages.items():
        if current in code.lower() or current in name.lower():
            display_name = f"{code} - {name}"
            if len(display_name) > 100:
                display_name = f"{code} - {name[:90]}..."
            choices.append(app_commands.Choice(name=display_name, value=code))
            
        if len(choices) >= 25:
            break
    
    if not choices:
        popular = ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh-CN"]
        for code in popular:
            name = languages.get(code, code)
            choices.append(app_commands.Choice(name=f"{code} - {name}", value=code))
    
    return choices

def translate_command():

    async def send_embed(context, embed: discord.Embed, *, ephemeral: bool = False) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await context.send(embed=embed)

    async def _translate_with_google_web(text: str, from_lang: str = "auto", to_lang: str = "en") -> dict:
        try:
            base_url = "https://translate.googleapis.com/translate_a/single"
            
            params = {
                "client": "gtx",
                "sl": from_lang,
                "tl": to_lang,
                "dt": ["t", "bd"],
                "q": text
            }
            
            param_string = "&".join([f"{k}={'&'.join(v) if isinstance(v, list) else v}" for k, v in params.items()])
            url = f"{base_url}?{param_string}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result_text = await response.text()
                        
                        try:
                            result_text = result_text.strip()
                            if result_text.startswith('[['):
                                data = json.loads(result_text)
                                
                                translated_text = ""
                                if data and len(data) > 0 and data[0]:
                                    for item in data[0]:
                                        if item and len(item) > 0:
                                            translated_text += item[0] if item[0] else ""
                                
                                detected_lang = from_lang
                                if len(data) > 2 and data[2]:
                                    detected_lang = data[2]
                                
                                return {
                                    "translatedText": translated_text.strip(),
                                    "detectedSourceLanguage": detected_lang
                                }
                        except:
                            pass
                    
            return None
        except Exception:
            return None


    @commands.hybrid_command(
        name="translate",
        description="Translate text to another language",
    )
    @app_commands.describe(
        text="The text to translate",
        to_lang="Target language (e.g., 'en', 'es', 'fr')",
        from_lang="Source language (leave empty for auto-detect)"
    )
    @app_commands.autocomplete(to_lang=language_autocomplete)
    @app_commands.autocomplete(from_lang=language_autocomplete)
    async def translate(self, context, text: str = None, to_lang: str = "en", from_lang: str = None):
        if not text or not text.strip():
            if context.message and context.message.reference and context.message.reference.resolved:
                replied_message = context.message.reference.resolved
                if hasattr(replied_message, 'content') and replied_message.content:
                    text = replied_message.content
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="The replied message has no text content to translate.",
                        color=0xE02B2B,
                    ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                    await send_embed(context, embed, ephemeral=True)
                    return
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Please provide text to translate or reply to a message with text.",
                    color=0xE02B2B,
                ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
                await send_embed(context, embed, ephemeral=True)
                return
        
        if to_lang not in languages:
            embed = discord.Embed(
                title="Error",
                description=f"Invalid target language code: `{to_lang}`. Use the autocomplete feature to see available languages.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        if from_lang and from_lang not in languages:
            embed = discord.Embed(
                title="Error",
                description=f"Invalid source language code: `{from_lang}`. Use the autocomplete feature to see available languages.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)
            return
        
        result = await _translate_with_google_web(text, from_lang or "auto", to_lang)
        
        if result and result.get("translatedText"):
            detected_lang = result.get("detectedSourceLanguage", from_lang or "auto")
            
            from_lang_name = languages.get(detected_lang, detected_lang)
            to_lang_name = languages.get(to_lang, to_lang)
            
            embed = discord.Embed(
                title="Translation",
                description=f"**Original:** {text}\n**Translated:** {result['translatedText']}",
                color=0x7289DA,
            )
            embed.set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            embed.set_footer(text=f"{from_lang_name} » {to_lang_name}")
            
            await send_embed(context, embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="Translation failed. Please try again later.",
                color=0xE02B2B,
            ).set_author(name="Utility", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await send_embed(context, embed, ephemeral=True)





    return translate