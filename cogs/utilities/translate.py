import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import asyncio
import re
import json
import urllib.parse


class Translate(commands.Cog, name="translate"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.languages = {
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

    async def send_embed(self, context: Context, embed: discord.Embed, *, ephemeral: bool = False, view: discord.ui.View = None) -> None:
        interaction = getattr(context, "interaction", None)
        if interaction is not None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=ephemeral, view=view)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral, view=view)
        else:
            await context.send(embed=embed, view=view)

    async def _translate_with_google_web(self, text: str, from_lang: str = "auto", to_lang: str = "en") -> dict:
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

    async def language_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        current = current.lower()
        choices = []
        
        for code, name in self.languages.items():
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
                name = self.languages.get(code, code)
                choices.append(app_commands.Choice(name=f"{code} - {name}", value=code))
        
        return choices

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
    async def translate(self, context: Context, text: str, to_lang: str = "en", from_lang: str = None):
        if not text.strip():
            embed = discord.Embed(
                title="Error",
                description="Please provide text to translate.",
                color=0xE02B2B,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await self.send_embed(context, embed, ephemeral=True)
            return
        
        if to_lang not in self.languages:
            embed = discord.Embed(
                title="Error",
                description=f"Invalid target language code: `{to_lang}`. Use the autocomplete feature to see available languages.",
                color=0xE02B2B,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await self.send_embed(context, embed, ephemeral=True)
            return
        
        if from_lang and from_lang not in self.languages:
            embed = discord.Embed(
                title="Error",
                description=f"Invalid source language code: `{from_lang}`. Use the autocomplete feature to see available languages.",
                color=0xE02B2B,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await self.send_embed(context, embed, ephemeral=True)
            return
        
        result = await self._translate_with_google_web(text, from_lang or "auto", to_lang)
        
        if result and result.get("translatedText"):
            detected_lang = result.get("detectedSourceLanguage", from_lang or "auto")
            
            from_lang_name = self.languages.get(detected_lang, detected_lang)
            to_lang_name = self.languages.get(to_lang, to_lang)
            
            embed = discord.Embed(
                title="Translation",
                color=0x7289DA,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            embed.add_field(name="Original", value=text, inline=False)
            embed.add_field(name="Translated", value=result["translatedText"], inline=False)
            embed.add_field(name="From", value=f"{detected_lang} ({from_lang_name})", inline=True)
            embed.add_field(name="To", value=f"{to_lang} ({to_lang_name})", inline=True)
            
            view = TranslateView(text, result["translatedText"], detected_lang, to_lang, self)
            await self.send_embed(context, embed, view=view)
        else:
            embed = discord.Embed(
                title="Error",
                description="Translation failed. Please try again later.",
                color=0xE02B2B,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await self.send_embed(context, embed, ephemeral=True)



class TranslateView(discord.ui.View):
    def __init__(self, original_text: str, translated_text: str, from_lang: str, to_lang: str, translate_cog):
        super().__init__(timeout=300)
        self.original_text = original_text
        self.translated_text = translated_text
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.translate_cog = translate_cog

    @discord.ui.button(label="Swap Languages", style=discord.ButtonStyle.secondary)
    async def swap_languages(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.from_lang == "auto":
            embed = discord.Embed(
                title="Cannot Swap",
                description="Cannot swap when source language is auto-detected. Please specify a source language first.",
                color=0xE02B2B,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        result = await self.translate_cog._translate_with_google_web(
            self.translated_text, self.from_lang, "en"
        )
        
        if result and result.get("translatedText"):
            from_lang_name = self.translate_cog.languages.get(self.from_lang, self.from_lang)
            to_lang_name = self.translate_cog.languages.get("en", "English")
            
            embed = discord.Embed(
                title="Translation (Swapped)",
                color=0x7289DA,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            embed.add_field(name="Original", value=self.translated_text, inline=False)
            embed.add_field(name="Translated", value=result["translatedText"], inline=False)
            embed.add_field(name="From", value=f"{self.from_lang} ({from_lang_name})", inline=True)
            embed.add_field(name="To", value=f"en ({to_lang_name})", inline=True)
            
            new_view = TranslateView(
                self.translated_text, 
                result["translatedText"], 
                self.from_lang, 
                "en", 
                self.translate_cog
            )
            
            await interaction.response.edit_message(embed=embed, view=new_view)
        else:
            embed = discord.Embed(
                title="Error",
                description="Failed to swap translation. Please try again later.",
                color=0xE02B2B,
            )
            embed.set_author(name="Translate", icon_url="https://yes.nighty.works/raw/8VLDcg.webp")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


async def setup(bot):
    await bot.add_cog(Translate(bot))