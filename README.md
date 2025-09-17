<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/bannerdark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/bannerlight.png">
  <img alt="Neos Helper Bot Banner" src="assets/bannerlight.png" style="width: 100%; height: auto;">
</picture>

<p align="center">
  <a href="https://github.com/neoarz/neos-helper-bot/blob/main/LICENSE.md">
    <img src="https://img.shields.io/github/license/neoarz/neos-helper-bot?label=License&color=5865F2&style=for-the-badge&labelColor=23272A" />
  </a>
  <a href="https://github.com/neoarz/neos-helper-bot/commits/main">
    <img src="https://img.shields.io/github/last-commit/neoarz/neos-helper-bot?label=Last%20Commit&color=5865F2&style=for-the-badge&labelColor=23272A" />
  </a>
  <a href="https://github.com/neoarz/neos-helper-bot">
    <img src="https://img.shields.io/github/languages/code-size/neoarz/neos-helper-bot?label=Code%20Size&color=5865F2&style=for-the-badge&labelColor=23272A" />
  </a>
</p>

> [!NOTE]
> This project is still in the making!!! I would appreciate if you gave this repo a star, that would mean a lot to me!


If you plan to use this template to make your own template or bot, you **have to**:

- Keep the credits, and a link to this repository in all the files that contains my code
- Keep the same license for unchanged code

See [the license file](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/master/LICENSE.md) for more
information, I reserve the right to take down any repository that does not meet these requirements.

## Support

Before requesting support, you should know that this template requires you to have at least a **basic knowledge** of
Python and the library is made for **advanced users**. Do not use this template if you don't know the
basics or some advanced topics such as OOP or async. [Here's](https://pythondiscord.com/pages/resources) a link for resources to learn python.

If you need some help for something, do not hesitate to create an issue over [here](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/issues), but don't forget the read the [frequently asked questions](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/wiki/Frequently-Asked-Questions) before.

All the updates of the template are available [here](UPDATES.md).

## Disclaimer

Slash commands can take some time to get registered globally, so if you want to test a command you should use
the `@app_commands.guilds()` decorator so that it gets registered instantly. Example:

```py
@commands.hybrid_command(
  name="command",
  description="Command description",
)
@app_commands.guilds(discord.Object(id=GUILD_ID)) # Place your guild ID here
```

When using the template you confirm that you have read the [license](LICENSE.md) and comprehend that I can take down
your repository if you do not meet these requirements.

## How to download it

This repository is now a template, on the top left you can simply click on "**Use this template**" to create a GitHub
repository based on this template.

Alternatively you can do the following:

- Clone/Download the repository
  - To clone it and get the updates you can definitely use the command
    `git clone`
- Create a Discord bot [here](https://discord.com/developers/applications)
- Get your bot token
- Invite your bot on servers using the following invite:
  https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS (
  Replace `YOUR_APPLICATION_ID_HERE` with the application ID and replace `PERMISSIONS` with the required permissions
  your bot needs that it can be get at the bottom of a this
  page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

## How to set up

To set up the token you will have to make use of the [`.env.example`](.env.example) file; you should rename it to `.env` and replace the `YOUR_BOT...` content with your actual values that match for your bot.

Alternatively you can simply create a system environment variable with the same names and their respective value.

## How to start

### The _"usual"_ way

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
python -m pip install -r requirements.txt
```

After that you can start it with

```
python bot.py
```

> **Note**: You may need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.

### Docker

Support to start the bot in a Docker container has been added. After having [Docker](https://docker.com) installed on your machine, you can simply execute:

```
docker compose up -d --build
```

> **Note**: `-d` will make the container run in detached mode, so in the background.

## Issues or Questions

If you have any issues or questions of how to code a specific command, you can:

- Join my Discord server [here](https://discord.gg/xj6y5ZaTMr)
- Post them [here](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/issues)

Me or other people will take their time to answer and help you.

## Versioning

We use [SemVer](http://semver.org) for versioning. For the versions available, see
the [tags on this repository](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/tags).

## Built With

- [Python 3.12.9](https://www.python.org/)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details
