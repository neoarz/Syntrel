import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
from io import BytesIO
from PIL import Image
import re
from datetime import datetime, timezone

ONE_MONTH = 2628000

vencord_fetch = 0
vencord_badges = {}
vencord_contributors = set()

quests_fetch = 0
quest_data = []

REGEX_DEVS = re.compile(r'id: (\d+)n(,\n\s+badge: false)?')

ACTIVITY_TYPE_NAMES = [
    "Playing",
    "Streaming",
    "Listening to",
    "Watching",
    "Custom Status",
    "Competing in",
    "Hang Status"
]

USER_FLAGS = {
    'STAFF': 1 << 0,
    'PARTNER': 1 << 1,
    'HYPESQUAD': 1 << 2,
    'BUG_HUNTER_LEVEL_1': 1 << 3,
    'HYPESQUAD_ONLINE_HOUSE_1': 1 << 6,
    'HYPESQUAD_ONLINE_HOUSE_2': 1 << 7,
    'HYPESQUAD_ONLINE_HOUSE_3': 1 << 8,
    'PREMIUM_EARLY_SUPPORTER': 1 << 9,
    'BUG_HUNTER_LEVEL_2': 1 << 14,
    'VERIFIED_DEVELOPER': 1 << 17,
    'CERTIFIED_MODERATOR': 1 << 18,
    'ACTIVE_DEVELOPER': 1 << 22
}

APPLICATION_FLAGS = {
    'APPLICATION_COMMAND_BADGE': 1 << 23,
    'AUTO_MODERATION_RULE_CREATE_BADGE': 1 << 6
}

BADGE_URLS = {
    'staff': 'https://discord.com/company',
    'partner': 'https://discord.com/partners',
    'certified_moderator': 'https://discord.com/safety',
    'hypesquad': 'https://discord.com/hypesquad',
    'hypesquad_house_1': 'https://discord.com/settings/hypesquad-online',
    'hypesquad_house_2': 'https://discord.com/settings/hypesquad-online',
    'hypesquad_house_3': 'https://discord.com/settings/hypesquad-online',
    'bug_hunter_level_1': 'https://support.discord.com/hc/en-us/articles/360046057772-Discord-Bugs',
    'bug_hunter_level_2': 'https://support.discord.com/hc/en-us/articles/360046057772-Discord-Bugs',
    'active_developer': 'https://support-dev.discord.com/hc/en-us/articles/10113997751447?ref=badge',
    'early_supporter': 'https://discord.com/settings/premium',
    'premium': 'https://discord.com/settings/premium',
    'bot_commands': 'https://discord.com/blog/welcome-to-the-new-era-of-discord-apps?ref=badge',
    'quest_completed': 'https://discord.com/settings/inventory'
}

BADGE_ICONS = {
    'staff': '<:discordstaff:1426051878155845702>',
    'partner': '<:discordpartner:1426051933608873986>',
    'certified_moderator': '<:discordmod:1426051921826943050>',
    'hypesquad': '<:hypesquadevents:1426051833536970852>',
    'hypesquad_house_1': '<:hypesquadbravery:1426051916739383297>',
    'hypesquad_house_2': '<:hypesquadbrilliance:1426051849433387068>',
    'hypesquad_house_3': '<:hypesquadbalance:1426051905179750495>',
    'bug_hunter_level_1': '<:discordbughunter1:1426052002193997895>',
    'bug_hunter_level_2': '<:discordbughunter2:1426052028257406987>',
    'active_developer': '<:activedeveloper:1426051981658685552>',
    'verified_developer': '<:discordbotdev:1426051827077480570>',
    'early_supporter': '<:discordearlysupporter:1426052023165517924>',
    'premium': '<:discordnitro:1426051911123206296>',
    'guild_booster_lvl1': '<:discordboost1:1426052007294144605>',
    'guild_booster_lvl2': '<:discordboost2:1426051986985582692>',
    'guild_booster_lvl3': '<:discordboost3:1426051991812964434>',
    'guild_booster_lvl4': '<:discordboost4:1426051955473645671>',
    'guild_booster_lvl5': '<:discordboost5:1426051960456609824>',
    'guild_booster_lvl6': '<:discordboost6:1426051976583712918>',
    'guild_booster_lvl7': '<:discordboost7:1426051965808410634>',
    'guild_booster_lvl8': '<:discordboost8:1426051844014342225>',
    'guild_booster_lvl9': '<:discordboost9:1426051855015743558>',
    'bot_commands': '<:supportscommands:1426051872476889171>',
    'automod': '<:automod:1426051939103146115>',
    'quest_completed': '<:quest:1426051817946611784>',
    'username': '<:username:1426051894371160115>',
    'premium_bot': '<:premiumbot:1426051888272638025>',
    'orb': '<:orb:1426051861605126289>',
    'bronze': '<:bronze:1426051866969772034>',
    'silver': '<:silver:1426051928575709286>',
    'gold': '<:gold:1426052012352737333>',
    'platinum': '<:platinum:1426052018040082545>',
    'diamond': '<:diamond:1426051944685895771>',
    'emerald': '<:emerald:1426051812313792537>',
    'ruby': '<:ruby:1426051838645637150>',
    'opal': '<:opal:1426051883247603762>'
}

ACTIVITY_TYPE_ICONS = {
    0: '<:gaming:1426409065701048451>',
    2: '<:music:1426409047132737586>',
    3: '<:watching:1426409475450863778>'
}

def format_username(user):
    if user.discriminator and user.discriminator != '0':
        return f'{user.name}#{user.discriminator}'
    return f'@{user.name}'

def get_default_avatar(user_id, discriminator=None):
    if discriminator and int(discriminator) > 0:
        index = int(discriminator) % 5
    else:
        index = (int(user_id) >> 22) % 6
    return f'https://cdn.discordapp.com/embed/avatars/{index}.png'

def snowflake_to_timestamp(snowflake):
    return ((int(snowflake) >> 22) + 1420070400000) / 1000

async def fetch_vencord_data():
    global vencord_fetch, vencord_badges, vencord_contributors
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://badges.vencord.dev/badges.json',
            headers={'User-Agent': 'HiddenPhox/userinfo'}
        ) as resp:
            badges = await resp.json()
            vencord_badges = badges
        
        async with session.get(
            'https://raw.githubusercontent.com/Vendicated/Vencord/main/src/utils/constants.ts'
        ) as resp:
            constants = await resp.text()
            vencord_contributors.clear()
            
            for match in REGEX_DEVS.finditer(constants):
                user_id, no_badge = match.groups()
                if no_badge or user_id == '0':
                    continue
                vencord_contributors.add(user_id)
    
    vencord_fetch = int(datetime.now().timestamp() * 1000) + 3600000

async def fetch_quest_data():
    global quests_fetch, quest_data
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://raw.githubusercontent.com/aamiaa/discord-api-diff/refs/heads/main/quests.json'
        ) as resp:
            quest_data = await resp.json()
    
    quests_fetch = int(datetime.now().timestamp() * 1000) + 3600000

async def get_user_data(bot, user_id):
    headers = {'Authorization': f'Bot {bot.http.token}'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://discord.com/api/v10/users/{user_id}',
            headers=headers
        ) as resp:
            if resp.status == 404:
                return None
            return await resp.json()

async def get_application_data(bot, app_id):
    headers = {'Authorization': f'Bot {bot.http.token}'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://discord.com/api/v10/applications/{app_id}/rpc',
            headers=headers
        ) as resp:
            if resp.status in [404, 403, 10002]:
                return None
            return await resp.json()

async def get_published_listing(bot, sku_id):
    headers = {'Authorization': f'Bot {bot.http.token}'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://discord.com/api/v10/store/published-listings/skus/{sku_id}',
            headers=headers
        ) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

def userinfo_command():
    @commands.hybrid_command(
        name="userinfo",
        description="Get information on a user.",
    )
    @app_commands.describe(
        user="User to get info for",
        user_id="User ID to get info for"
    )
    async def userinfo(self, context, user: discord.User = None, user_id: str = None):
        await context.defer()
        
        bot = self.bot
        target_user = user if user else context.author
        
        if user_id:
            try:
                target_user = await bot.fetch_user(int(user_id))
            except:
                await context.send('User not found.')
                return
        
        user_data = await get_user_data(bot, target_user.id)
        if not user_data:
            await context.send('Failed to fetch user data.')
            return
        
        guild = context.guild
        member = guild.get_member(target_user.id) if guild else None
        
        if int(datetime.now().timestamp() * 1000) > vencord_fetch:
            try:
                await fetch_vencord_data()
            except:
                pass
        
        if int(datetime.now().timestamp() * 1000) > quests_fetch:
            try:
                await fetch_quest_data()
            except:
                pass
        
        badges = []
        flags = user_data.get('public_flags', 0)
        
        if str(target_user.id) == '1015372540937502851':
            badges.append(f"[{BADGE_ICONS['staff']}]({BADGE_URLS['staff']})")
            badges.append(f"[{BADGE_ICONS['partner']}]({BADGE_URLS['partner']})")
            badges.append(f"[{BADGE_ICONS['certified_moderator']}]({BADGE_URLS['certified_moderator']})")
            badges.append(f"[{BADGE_ICONS['hypesquad_house_1']}]({BADGE_URLS['hypesquad_house_1']})")
            badges.append(f"[{BADGE_ICONS['bug_hunter_level_2']}]({BADGE_URLS['bug_hunter_level_2']})")
            badges.append(BADGE_ICONS['verified_developer'])
            badges.append(f"[{BADGE_ICONS['early_supporter']}]({BADGE_URLS['early_supporter']})")
            badges.append(f"[{BADGE_ICONS['guild_booster_lvl9']}]({BADGE_URLS['premium']})")
            badges.append(f"[{BADGE_ICONS['quest_completed']}]({BADGE_URLS['quest_completed']})")
            badges.append(BADGE_ICONS['username'])
        elif str(target_user.id) == '1376728824108286034':
            badges.append(BADGE_ICONS['automod'])
            badges.append(BADGE_ICONS['verified_developer'])
            badges.append(BADGE_ICONS['premium_bot'])
        elif flags & USER_FLAGS['STAFF']:
            badges.append(f"[{BADGE_ICONS['staff']}]({BADGE_URLS['staff']})")
        if flags & USER_FLAGS['PARTNER']:
            badges.append(f"[{BADGE_ICONS['partner']}]({BADGE_URLS['partner']})")
        if flags & USER_FLAGS['CERTIFIED_MODERATOR']:
            badges.append(f"[{BADGE_ICONS['certified_moderator']}]({BADGE_URLS['certified_moderator']})")
        if flags & USER_FLAGS['HYPESQUAD']:
            badges.append(f"[{BADGE_ICONS['hypesquad']}]({BADGE_URLS['hypesquad']})")
        if flags & USER_FLAGS['HYPESQUAD_ONLINE_HOUSE_1']:
            badges.append(f"[{BADGE_ICONS['hypesquad_house_1']}]({BADGE_URLS['hypesquad_house_1']})")
        if flags & USER_FLAGS['HYPESQUAD_ONLINE_HOUSE_2']:
            badges.append(f"[{BADGE_ICONS['hypesquad_house_2']}]({BADGE_URLS['hypesquad_house_2']})")
        if flags & USER_FLAGS['HYPESQUAD_ONLINE_HOUSE_3']:
            badges.append(f"[{BADGE_ICONS['hypesquad_house_3']}]({BADGE_URLS['hypesquad_house_3']})")
        if flags & USER_FLAGS['BUG_HUNTER_LEVEL_1']:
            badges.append(f"[{BADGE_ICONS['bug_hunter_level_1']}]({BADGE_URLS['bug_hunter_level_1']})")
        if flags & USER_FLAGS['BUG_HUNTER_LEVEL_2']:
            badges.append(f"[{BADGE_ICONS['bug_hunter_level_2']}]({BADGE_URLS['bug_hunter_level_2']})")
        if flags & USER_FLAGS['ACTIVE_DEVELOPER']:
            badges.append(f"[{BADGE_ICONS['active_developer']}]({BADGE_URLS['active_developer']})")
        if flags & USER_FLAGS['VERIFIED_DEVELOPER']:
            badges.append(BADGE_ICONS['verified_developer'])
        if flags & USER_FLAGS['PREMIUM_EARLY_SUPPORTER']:
            badges.append(f"[{BADGE_ICONS['early_supporter']}]({BADGE_URLS['early_supporter']})")
        
        avatar_hash = user_data.get('avatar', '')
        banner_hash = user_data.get('banner')
        if (banner_hash or (avatar_hash and avatar_hash.startswith('a_'))) and not user_data.get('bot'):
            badges.append(f"[{BADGE_ICONS['premium']}]({BADGE_URLS['premium']})")
        
        if member and member.premium_since:
            boosting_since = member.premium_since
            delta = (datetime.now(timezone.utc) - boosting_since).total_seconds()
            icon = BADGE_ICONS['guild_booster_lvl1']
            
            if delta >= ONE_MONTH * 24:
                icon = BADGE_ICONS['guild_booster_lvl9']
            elif delta >= ONE_MONTH * 18:
                icon = BADGE_ICONS['guild_booster_lvl8']
            elif delta >= ONE_MONTH * 15:
                icon = BADGE_ICONS['guild_booster_lvl7']
            elif delta >= ONE_MONTH * 12:
                icon = BADGE_ICONS['guild_booster_lvl6']
            elif delta >= ONE_MONTH * 9:
                icon = BADGE_ICONS['guild_booster_lvl5']
            elif delta >= ONE_MONTH * 6:
                icon = BADGE_ICONS['guild_booster_lvl4']
            elif delta >= ONE_MONTH * 3:
                icon = BADGE_ICONS['guild_booster_lvl3']
            elif delta >= ONE_MONTH * 2:
                icon = BADGE_ICONS['guild_booster_lvl2']
            
            badges.append(f"[{icon}]({BADGE_URLS['premium']})")
        
        bot_deleted = False
        if user_data.get('bot'):
            app_data = await get_application_data(bot, target_user.id)
            if app_data:
                app_flags = app_data.get('flags', 0)
                if app_flags & APPLICATION_FLAGS['APPLICATION_COMMAND_BADGE']:
                    badges.append(f"[{BADGE_ICONS['bot_commands']}]({BADGE_URLS['bot_commands']})")
                if app_flags & APPLICATION_FLAGS['AUTO_MODERATION_RULE_CREATE_BADGE']:
                    badges.append(BADGE_ICONS['automod'])
            else:
                bot_deleted = True
            
            if user_data.get('system'):
                bot_deleted = False
        
        quest_decoration_name = None
        avatar_decoration = user_data.get('avatar_decoration_data')
        if avatar_decoration and avatar_decoration.get('sku_id'):
            for quest in quest_data:
                config = quest.get('config', {})
                rewards = config.get('rewards_config', {}).get('rewards', []) or config.get('rewards', [])
                
                for reward in rewards:
                    if reward.get('type') == 3 and reward.get('sku_id') == avatar_decoration['sku_id']:
                        quest_decoration_name = (reward.get('name') or reward.get('messages', {}).get('name') or '*Unknown*').replace('Avatar Decoration', 'Avatar Deco')
                        badges.append(f"[{BADGE_ICONS['quest_completed']}]({BADGE_URLS['quest_completed']})")
                        break
                if quest_decoration_name:
                    break
        elif avatar_decoration and (avatar_decoration.get('expires_at') or avatar_decoration.get('sku_id') == '1226939756617793606'):
            badges.append(f"[{BADGE_ICONS['quest_completed']}]({BADGE_URLS['quest_completed']})")
        
        if str(target_user.id) in vencord_contributors:
            badges.append('[<:VencordContributor:1273333728709574667>](https://vencord.dev)')
        
        if user_data.get('legacy_username'):
            badges.append(BADGE_ICONS['username'])
        
        if user_data.get('bot') and user_data.get('approximated_guild_count'):
            badges.append(BADGE_ICONS['premium_bot'])
        
        profile_effect = user_data.get('profile_effect')
        if profile_effect:
            effect_id = profile_effect.get('id')
            if effect_id:
                orb_tier = None
                
                if '1139323098643333240' in effect_id:
                    orb_tier = 'opal'
                elif '1139323095841308733' in effect_id:
                    orb_tier = 'ruby'
                elif '1139323090842013756' in effect_id:
                    orb_tier = 'emerald'
                elif '1139323087608832090' in effect_id:
                    orb_tier = 'diamond'
                elif '1144286544523669516' in effect_id:
                    orb_tier = 'platinum'
                elif '1139323084127289374' in effect_id:
                    orb_tier = 'gold'
                elif '1139323078435717220' in effect_id:
                    orb_tier = 'silver'
                elif '1139323075214307448' in effect_id:
                    orb_tier = 'bronze'
                else:
                    orb_tier = 'orb'
                
                if orb_tier:
                    badges.append(BADGE_ICONS[orb_tier])
        
        default_avatar = get_default_avatar(target_user.id, user_data.get('discriminator', '0'))
        avatar_url = target_user.avatar.url if target_user.avatar else default_avatar
        
        banner_url = None
        banner_file = None
        original_banner_link = None
        if banner_hash:
            is_animated = banner_hash.startswith('a_')
            ext = 'gif' if is_animated else 'png'
            original_banner_url = f'https://cdn.discordapp.com/banners/{target_user.id}/{banner_hash}.{ext}?size=4096'
            original_banner_link = original_banner_url
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(original_banner_url) as resp:
                        if resp.status == 200:
                            banner_data = await resp.read()
                            img = Image.open(BytesIO(banner_data))
                            
                            if img.width < 1100:
                                new_width = 1100
                                aspect_ratio = img.height / img.width
                                new_height = int(new_width * aspect_ratio)
                                
                                if is_animated:
                                    frames = []
                                    durations = []
                                    
                                    try:
                                        while True:
                                            frame = img.copy().convert('RGBA')
                                            frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                                            frames.append(frame)
                                            durations.append(img.info.get('duration', 100))
                                            img.seek(img.tell() + 1)
                                    except EOFError:
                                        pass
                                    
                                    output = BytesIO()
                                    frames[0].save(
                                        output,
                                        format='GIF',
                                        save_all=True,
                                        append_images=frames[1:],
                                        duration=durations,
                                        loop=0,
                                        optimize=False
                                    )
                                    output.seek(0)
                                    banner_file = discord.File(output, filename='banner.gif')
                                    banner_url = 'attachment://banner.gif'
                                else:
                                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                                    
                                    output = BytesIO()
                                    img.save(output, format='PNG')
                                    output.seek(0)
                                    banner_file = discord.File(output, filename='banner.png')
                                    banner_url = 'attachment://banner.png'
                            else:
                                banner_url = original_banner_url
            except:
                banner_url = original_banner_url
        
        images = [f'[Avatar]({avatar_url})']
        
        if banner_url:
            images.append(f'[Banner]({original_banner_link})')
        
        if avatar_decoration:
            await get_published_listing(bot, avatar_decoration['sku_id'])
            decoration_url = f"https://cdn.discordapp.com/avatar-decoration-presets/{avatar_decoration['asset']}.png?size=4096&passthrough=true"
            images.append(f'[Avatar Deco]({decoration_url})')
        
        collectibles = user_data.get('collectibles')
        if collectibles and collectibles.get('nameplate'):
            nameplate = collectibles['nameplate']
            nameplate_asset = nameplate['asset']
            images.append(f'[Nameplate](https://cdn.discordapp.com/assets/collectibles/{nameplate_asset}static.png)')
        
        mutual_guilds = [g for g in bot.guilds if g.get_member(target_user.id)]
        display_name = user_data.get('global_name') or user_data.get('username')
        
        desc_lines = [
            f"# {member.nick if member and member.nick else display_name}",
            f"{format_username(target_user).replace('@', '')} • <@{target_user.id}>"
        ]
        
        subline = ""
        if badges:
            subline += ''.join(badges)
        
        activity_lines = []
        if member and member.activities:
            for activity in member.activities:
                if activity.type == discord.ActivityType.custom:
                    activity_lines.append(ACTIVITY_TYPE_NAMES[4])
                elif activity.type in [discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.watching]:
                    name = activity.name
                    activity_lines.append(
                        f"{ACTIVITY_TYPE_ICONS.get(activity.type.value, '')} {ACTIVITY_TYPE_NAMES[activity.type.value]} **{name}**".strip()
                    )
        
        if subline:
            desc_lines.append(subline)
        
        if mutual_guilds:
            desc_lines.append(f"-# {len(mutual_guilds)} Bot Mutual Server{'s' if len(mutual_guilds) > 1 else ''}")
        else:
            desc_lines.append('')
        
        is_system = user_data.get('system') or user_data.get('discriminator') == '0000'
        
        if bot_deleted and not is_system:
            desc_lines.append("*This bot's application has been deleted*\n-# (or app ID and user ID desync)")
        if is_system:
            desc_lines.append('**System account**')
        desc_lines.append('')
        
        if activity_lines:
            desc_lines.extend(activity_lines)
        
        embed = discord.Embed(
            color=0x7289DA,
            description='\n'.join(desc_lines)
        )
        
        primary_guild = user_data.get('primary_guild')
        if primary_guild and primary_guild.get('identity_guild_id'):
            clan_badge_url = f"https://cdn.discordapp.com/clan-badges/{primary_guild['identity_guild_id']}/{primary_guild['badge']}.png?size=4096"
            embed.set_author(name=primary_guild.get('tag', ''), icon_url=clan_badge_url)
        else:
            embed.set_author(name="User Information", icon_url="https://yes.nighty.works/raw/gSxqzV.png")
        
        if member and member.nick and member.nick != display_name:
            embed.title = display_name
        
        embed.set_thumbnail(url=avatar_url)
        
        if banner_url:
            embed.set_image(url=banner_url)
        
        created_timestamp = int(snowflake_to_timestamp(target_user.id))
        created_date = f"<t:{created_timestamp}:F>"
        
        embed.add_field(name='Created Date', value=created_date, inline=False)
        
        if member and hasattr(member, 'joined_at') and member.joined_at:
            joined_timestamp = int(member.joined_at.timestamp())
            join_date = f"<t:{joined_timestamp}:F>"
            embed.add_field(name='Join Date', value=join_date, inline=False)
        
        is_bot = user_data.get('bot', False)
        embed.add_field(name='Is Bot', value='True' if is_bot else 'False', inline=True)
        
        vc_badges = vencord_badges.get(str(target_user.id))
        if vc_badges:
            vc_badge_list = [f'"[{b["tooltip"]}]({b["badge"]})"' for b in vc_badges]
            embed.add_field(
                name=f'Vencord Donator Badge{"s" if len(vc_badges) > 1 else ""} ({len(vc_badges)})' if len(vc_badges) > 1 else 'Vencord Donator Badge',
                value=', '.join(vc_badge_list),
                inline=True
            )
        
        if member and member.roles[1:]:
            roles = sorted(member.roles[1:], key=lambda r: r.position, reverse=True)
            role_mentions = [f'<@&{r.id}>' for r in roles]
            role_list = ' '.join(role_mentions)
            
            if len(role_list) > 1024:
                truncated_roles = []
                current_length = 0
                for mention in role_mentions:
                    if current_length + len(mention) + 1 > 1020:
                        break
                    truncated_roles.append(mention)
                    current_length += len(mention) + 1
                role_list = ' '.join(truncated_roles) + ' ...'
            
            embed.add_field(name=f'Roles ({len(member.roles) - 1})', value=role_list, inline=False)
        
        if images:
            embed.add_field(name='\u200b', value='\u3000'.join(images), inline=False)
        
        embed.set_footer(text=f'ID: {target_user.id}')
        
        if banner_file:
            await context.send(embed=embed, file=banner_file)
        else:
            await context.send(embed=embed)
    
    return userinfo

