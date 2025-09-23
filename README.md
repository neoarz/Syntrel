<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/bannerdark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/bannerlight.png">
    <img alt="Syntrel Discord Bot Banner" src="assets/bannerlight.png" style="width: 80%; height: auto;">
  </picture>
</div>

<br>

Modern, modular Discord bot built with `discord.py` 2.6+, async SQLite, and a clean cog architecture.

### Features

| Command group | Subcommands |
| --- | --- |
| owner | `sync`, `cog_management`, `shutdown`, `say`, `invite` |
| general | `help`, `botinfo`, `serverinfo`, `ping`, `feedback`, `uptime` |
| fun | `randomfact`, `coinflip`, `rps`, `8ball`, `minesweeper` |
| moderation | `kick`, `ban`, `nick`, `purge`, `hackban`, `warnings`, `archive` |
| sidestore | `sidestore`, `refresh`, `code`, `crash`, `pairing`, `server`, `half`, `sparse`, `afc`, `udid` |
| idevice | `idevice`, `noapps` |
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
