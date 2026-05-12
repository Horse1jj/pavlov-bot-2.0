# pavlov-bot-2.0
A Pavlov Shack Discord RCON bot ported for modern Python and `discord.py`.



Please credit the makers of this product in a way, Coco111, foste1jj and shareholder chunkybaba22.

## Overview
This bot connects Discord to Pavlov server RCON via `async-pavlov` and exposes admin, moderator, and public commands through Discord.

The bot uses:
- `main.py` to load configuration and cogs.
- `config.json` for Discord prefix, bot token, and hybrid command mode.
- `servers.json` to define one or more Pavlov server connections and role permissions.
- `cogs/` to implement command modules and UI interactions.
- `docker-compose.yml` to run the bot in Docker if desired.

---

## Requirements
Install these Python packages before running the bot:
- `discord.py`
- `colorama`
- `async-pavlov`
- `python-dotenv`

The repository also uses standard libraries: `json`, `os`, `asyncio`, and `platform`.

Install dependencies with:

```powershell
pip install -r packages.txt
```

If you prefer a manual installation:

```powershell
pip install discord.py colorama async-pavlov python-dotenv
```

---

## Configuration
### `config.json`
The bot reads `config.json` before startup.

Example structure:

```json
{"prefix": ";", "token": "TokenHere", "default_server": "default","hybrid": false}
```

Fields:
- `prefix`: Command prefix for Discord commands.
- `token`: Discord bot token
- `default_server`: Default server name if you want to refer to one server by default in custom code.
- `hybrid`: when `true`, The bot will use hybrid commands (slash + message commands) instead of plain text commands.

### `servers.json`
This file maps server names to RCON connection settings and Discord role IDs.

Example entry:

```json
{
  "my-server": {
    "modroles": [123456789012345678],
    "adminroles": [987654321098765432],
    "ip": "127.0.0.1",
    "port": 9101,
    "password": "your_rcon_password"
  }
}
```

Fields:
- `modroles`: Discord role IDs allowed to use moderator commands.
- `adminroles`: Discord role IDs allowed to use admin commands.
- `ip`: Pavlov server IP.
- `port`: Pavlov server RCON port.
- `password`: RCON password.

> Use raw numeric role IDs from your server settings.

---

## Starting the Bot
### Local Python run

1.clone the respiratory  

```powershell
  git clone https://github.com/Horse1jj/pavlov-bot-2.0
```

2. Confirm `config.json` contains your Discord bot token.

3. Confirm `servers.json` contains valid server entries.

4. Start the bot:

```powershell
python main.py
```

If the bot starts successfully, you will see a banner and the loaded cogs.

### Docker run
The repository includes a simple `docker-compose.yml` service.

Build and run with:

```powershell
docker-compose up -d --build
```

The Docker setup mounts the repository into `/app` and uses `/app/config.json`.

---

## Bot Management
### Loading modules
The bot automatically loads every `.py` file inside `cogs/` when starting.

Current cogs:
- `admin.py` — Server administration commands.
- `mod.py` — Moderator commands.
- `civilians.py` — Public player and ping commands.
- `panel.py` — Interactive admin menu.
- `help.py` — Command help output.
- `error-handler.py` — Command error handling.
- `hybrid-sync.py` — Hybrid command sync support.

### Common maintenance tasks
- Update bot token: edit `config.json` → `token`
- Add or change a server: edit `servers.json`
- Change prefix or hybrid mode: edit `config.json`
- Add a new command file: place it in `cogs/` and restart the bot
- Restart bot after config changes: stop and rerun `python main.py` or `docker-compose restart`

---

## Commands
The bot uses the prefix from `config.json`. If `prefix` is `;`, commands look like `;help`, `;players`, etc.

### Public commands
- `help` — Show available commands and usage
- `players <server_name>` — List players for a given server
- `ping` — Check bot responsiveness

### Moderator commands
- `kick <UniqueID> <server_name>`
- `ban <UniqueID> <server_name>`
- `unban <UniqueID> <server_name>`
- `kill <UniqueID> <server_name>`
- `slap <UniqueID> <server_name> [damage]`
- `switchteam <UniqueID> <TeamID> <server_name>`
- `teleport <SourceID> <TargetID> <server_name>`
- `giveitem <UniqueID> <ItemID> <server_name> [amount]`
- `givecash <UniqueID> <amount> <server_name>`
- `gag <UniqueID> <server_name> <True/False>`
- `setplayerskin <UniqueID> <SkinID> <server_name>`
- `clearemptyvehicles <server_name>`
- `inspectplayer <UniqueID> <server_name>`
- `inspectteam <TeamID> <server_name>`

### Admin commands
- `switchmap <MapID> <GameMode>`
- `maplist`
- `addmaprotation <MapID> <GameMode>`
- `removemaprotation <MapID> <GameMode>`
- `setmaxplayers <Amount>`
- `updateservername <Name>`
- `shutdownserver`
- `pausematch <Seconds>`
- `resetsnd`
- `setpin <PinNumber>`
- `settimelimit <Seconds>`
- `shownametags <True/False>`
- `enablecompmode <True/False>`
- `enablewhitelist <True/False>`
- `setlimitedammotype <0-5>`
- `addmod <UniqueID>`
- `removemod <UniqueID>`
- `menu` - Opens the interactive admin menu

### TTT commands
- `tttsetrole <UniqueID> <RoleID> <server_name>`
- `tttsetkarma <UniqueID> <Amount> <server_name>`
- `tttpausetimer <True/False> <server_name>`
- `tttendround <server_name>`
- `tttflushkarma <server_name>`
- `tttgivecredits <UniqueID> <Amount> <server_name>`

> Use `;help` in Discord to get the built-in command list embed.

---

## Permissions and Roles
Permissions are driven by `servers.json`.
- `modroles` Controls moderator command access.
- `adminroles` Controls admin command access.

Each command checks the invoking user's Discord roles against the configured role IDs for the target server.

---

## Troubleshooting
- If the bot fails to start, verify `config.json` is valid JSON and the `token` is correct.
- If a command fails, confirm the server name exists in `servers.json` and that the user has the correct role.
- If RCON commands fail, confirm the server IP, port, and password are correct.
- If Docker fails, ensure your Docker daemon is running and `docker-compose` is installed.

---

## Notes
- The bot loads every cog from `cogs/` on startup.
- `menu` Opens an interactive admin UI with server and player selection.
- `hybrid` Mode enables slash commands if set to `true` in `config.json`.
- `custom` Used for sending commands that are not listed in the normal commands.

---

# 1.10.0 plans 

- flush command 
- servers command 
- embedded responses 
- specificy what perms are needed instead of current responses 

