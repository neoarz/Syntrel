<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/bannerdark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/bannerlight.png">
    <img alt="Syntrel Discord Bot Banner" src="assets/bannerlight.png" style="width: 80%; height: auto;">
  </picture>
</div>

<br>

<div align="center">

**All in one discord bot for helping with [SideStore](https://discord.gg/3DwCwpBHfv), [idevice](https://discord.gg/ZnNcrRT3M8), [MeloNX](https://discord.gg/Q4VkbkYfmk), and more.**

</div>

<br>

## Commands

![Total Commands](https://img.shields.io/badge/Total%20Commands-71-5865F2)

| Command&nbsp;group | Subcommands |
| ------------ | --- |
| ungrouped | `help`, `botinfo` |
| owner | `sync`, `cog_management`, `shutdown`, `say`, `invite`, `logs` |
| general | `serverinfo`, `ping`, `feedback`, `uptime`, `userinfo` |
| fun | `randomfact`, `coinflip`, `rps`, `8ball`, `minesweeper` |
| moderation | `kick`, `ban`, `nick`, `purge`, `hackban`, `warnings`, `archive`, `timeout` |
| sidestore | `help`, `refresh`, `code`, `crash`, `pairing`, `server`, `half`, `sparse`, `afc`, `udid` |
| idevice | `help`, `noapps`, `errorcode`, `developermode`, `mountddi` |
| melonx | `help`, `transfer`, `mods`, `gamecrash`, `requirements`, `error`, `26`, `legal` |
| events | `baitbot` |
| miscellaneous | `keanu`, `labubu`, `piracy`, `tryitandsee`, `rickroll`, `dontasktoask`, `support`, `depart`, `docs` `sigma`, `duck`, `silly`, `color` |
| utilities | `translate`, `codepreview`, `dictionary` |
| media | `download`, `mcquote`, `img2gif`, `tweety`, `tts` |


## Download

<div align="left">
  <a href="https://discord.com/oauth2/authorize?client_id=1376728824108286034" target="_blank" rel="noopener noreferrer">
    <img src="assets/download.png" alt="Download" style="width: 290px; height: auto;">
  </a>
</div>


## Contributing

Contributions are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

## License

Dual licensed project, see [`LICENSE`](LICENSE) file for detailed attribution information

## Hosting

### Linux

1. Download Python

```console
sudo apt install python
```

2. Install Docker 

```console
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. How to get [Discord bot token](https://allaboutcookies.org/discord-bot-hosting-guide) (Only look through steps 1-4)

4. Add your configurarion to .env.example and rename to .env

5. Install Docker dependencies And run Discord bot

```console
docker compose up
```

### Windows

1. Install [Python](https://www.python.org/downloads/)

2. Install [Docker](https://docs.docker.com/desktop/setup/install/windows-install/)

3. How to get [Discord bot token](https://allaboutcookies.org/discord-bot-hosting-guide) (Only look through steps 1-4)

4. Add your configuration to .env.example and rename to .env

5. Install Docker dependencies And run Discord bot

```console
docker compose up
```

### MacOS

1. Install [Python](https://www.python.org/downloads/)

2. Install [Docker](https://docs.docker.com/desktop/setup/install/mac-install/)

3. How to get [Discord bot token](https://allaboutcookies.org/discord-bot-hosting-guide) (Only look through steps 1-4)

4. Add your configuration to .env.example and rename to .env

5. Install Docker dependencies And run Discord bot

```console
docker compose up
```

## MacOS (Brew)

1. Install Brew

```console
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install python

```console
brew install python
```

3. Install Docker

```console
brew intall docker
```

5. How to get [Discord bot token](https://allaboutcookies.org/discord-bot-hosting-guide) (Only look through steps 1-4)

6. Add your configuration to .env.example and rename to .env

7. Install Docker dependencies And run Discord bot

```console
docker compose up
```