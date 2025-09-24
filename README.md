<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/bannerdark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/bannerlight.png">
    <img alt="Syntrel Discord Bot Banner" src="assets/bannerlight.png" style="width: 80%; height: auto;">
  </picture>
</div>

<br>

<div align="center">

All in one discord bot for helping with [SideStore](https://discord.gg/3DwCwpBHfv), [idevice](https://discord.gg/ZnNcrRT3M8), and more.

</div>

> [!NOTE]
> **Download**
> 
> This bot is heavily customized and may not be a good starting point template wise. But if you wanna use this bot, or maybe add to your own server, here is the download link: 
> 
> [https://discord.com/oauth2/authorize?client_id=1376728824108286034](https://discord.com/oauth2/authorize?client_id=1376728824108286034)

### Commands

| Command group | Subcommands |
| --- | --- |
| owner | `sync`, `cog_management`, `shutdown`, `say`, `invite` |
| general | `help`, `botinfo`, `serverinfo`, `ping`, `feedback`, `uptime` |
| fun | `randomfact`, `coinflip`, `rps`, `8ball`, `minesweeper` |
| moderation | `kick`, `ban`, `nick`, `purge`, `hackban`, `warnings`, `archive` |
| sidestore | `sidestore`, `refresh`, `code`, `crash`, `pairing`, `server`, `half`, `sparse`, `afc`, `udid` |
| idevice | `idevice`, `noapps`, `errorcode` |
| miscellaneous | `keanu`, `labubu` |

Additional:
- Async SQLite database initialization via `aiosqlite`
- Structured logging to console and `discord.log`
- Lightweight status rotation

### Requirements
- Python 3.13+
- A Discord bot token

### Configuration
- **TOKEN**: Discord bot token
- **PREFIX**: Message command prefix (slash commands are also supported)
- **INVITE_LINK**: Shown by owner `invite` command
- **DISABLED_COGS**: Comma-separated list of cogs to skip (case-insensitive). Examples:
  - `general.context_menus`
  - `fun.minesweeper`
  - `owner.say`
  - Full path style also supported: `general.context_menus, moderation.ban`

### Commands overview
- **Hybrid commands**: Many commands are hybrid (both prefix and slash). If a user lacks permission for a message command in a server, the UI will suggest using the slash command instead.
- **Slash commands**: Registered via the loaded cogs; run `/sync` (owner) to force-sync if needed.

 

### Data and logging
- **Database**: `database/database.db` is initialized automatically from `database/schema.sql` on startup.
- **Logs**: Console output is colorized; a structured log is written to `discord.log` each run.

### Permissions and intents
The bot enables default intents plus `message_content`, `bans`, and DM-related intents. Ensure these are enabled in the Developer Portal for your application if required.

### Contributing
Contributions are welcome. See `CONTRIBUTING.md` for guidelines.

<br>

## License

Dual licensed project, see [LICENSE](LICENSE) file for detailed attribution information
