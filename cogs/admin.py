import json
import shlex

from discord.ext import commands

from utils.permissions import has_server_permission
from utils.sender_function import send_rcon
from utils.server_config import load_servers, resolve_server_name

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

SERVERS = load_servers()

cmd = commands.hybrid_command if config.get("hybrid") else commands.command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _resolve_custom_target(self, raw_input: str) -> tuple[str, str]:
        raw_input = raw_input.strip()
        if not raw_input:
            raise ValueError("Please provide an RCON command to send.")

        try:
            parts = shlex.split(raw_input)
        except ValueError as exc:
            raise ValueError(f"Could not parse custom command: {exc}") from exc

        server_name = None
        command_parts = parts

        if parts and parts[-1] in SERVERS:
            server_name = parts[-1]
            command_parts = parts[:-1]

        if not command_parts:
            raise ValueError("Please provide an RCON command after the server name.")

        return resolve_server_name(server_name, config=config), " ".join(command_parts)

    @cmd(name="switchmap", help="Immediately switches to a map")
    async def switchmap(self, ctx, map_id: str, game_mode: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "SwitchMap", map_id, game_mode)
            await ctx.send(f"Switched to map `{map_id}` with game mode `{game_mode}` on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to switch map: `{e}`")

    @cmd(name="maplist", help="Returns the current map rotation")
    async def maplist(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            response = await send_rcon(server_name, "MapList")
            await ctx.send(f"Current map rotation on `{server_name}`:\n```\n{response}\n```")
        except Exception as e:
            await ctx.send(f"Failed to get maplist: `{e}`")

    @cmd(name="addmaprotation", help="Adds a map to the rotation")
    async def addmaprotation(self, ctx, map_id: str, game_mode: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "AddMapRotation", map_id, game_mode)
            await ctx.send(f"Added map `{map_id}` with game mode `{game_mode}` to the rotation on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to add map to rotation: `{e}`")

    @cmd(name="removemaprotation", help="Removes a map from the rotation")
    async def removemaprotation(self, ctx, map_id: str, game_mode: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "RemoveMapRotation", map_id, game_mode)
            await ctx.send(f"Removed map `{map_id}` with game mode `{game_mode}` from the rotation on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to remove map from rotation: `{e}`")

    @cmd(name="setmaxplayers", help="Sets the server slot count (1-24)")
    async def setmaxplayers(self, ctx, amount: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        if amount < 1 or amount > 24:
            await ctx.send("Player count must be between 1 and 24")
            return
        try:
            await send_rcon(server_name, "SetMaxPlayers", str(amount))
            await ctx.send(f"Set maximum players to `{amount}` on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set max players: `{e}`")

    @cmd(name="updateservername", help="Changes the server name")
    async def updateservername(self, ctx, *, name: str):
        parts = name.split(maxsplit=1)
        if len(parts) == 2 and parts[0] in SERVERS:
            server_name, name = parts
        else:
            server_name = None

        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "UpdateServerName", name)
            await ctx.send(f"Updated server name to `{name}` on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to update server name: `{e}`")


    @cmd(name="rotatemap", aliases=["rotateMap"], help="Rotates to the next map")
    async def rotatemap(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "RotateMap", "Rotate map result", require_mod=True)

    @cmd(name="moderatorlist", help="Lists server moderators")
    async def moderatorlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "ModeratorList", "Moderator list", require_mod=True)

    @cmd(name="shutdownserver", help="Immediately shuts down the server")
    async def shutdownserver(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "ShutdownServer")
            await ctx.send(f"Server `{server_name}` is shutting down...")
        except Exception as e:
            await ctx.send(f"Failed to shutdown server: `{e}`")

    @cmd(name="pausematch", help="Pauses the match for a set amount of seconds")
    async def pausematch(self, ctx, seconds: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "PauseMatch", str(seconds))
            await ctx.send(f"Paused match for `{seconds}` seconds on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to pause match: `{e}`")

    @cmd(name="resetsnd", help="Resets the current SND match")
    async def resetsnd(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "ResetSND")
            await ctx.send(f"SND match has been reset on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to reset SND match: `{e}`")

    @cmd(name="setpin", help="Sets or removes the server join pin")
    async def setpin(self, ctx, pin_number: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "SetPin", pin_number)
            if pin_number.lower() == "none":
                await ctx.send(f"Server join pin has been removed on `{server_name}`")
            else:
                await ctx.send(f"Server join pin has been set to `{pin_number}` on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set pin: `{e}`")

    @cmd(name="settimelimit", help="Sets the match time limit")
    async def settimelimit(self, ctx, seconds: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "SetTimeLimit", str(seconds))
            await ctx.send(f"Match time limit has been set to `{seconds}` seconds on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set time limit: `{e}`")

    @cmd(name="shownametags", help="Enables or disables friendly nametags")
    async def shownametags(self, ctx, enabled: bool, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "ShowNametags", str(enabled))
            await ctx.send(f"Friendly nametags have been {'enabled' if enabled else 'disabled'} on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set nametags: `{e}`")

    @cmd(name="enablecompmode", help="Enables or disables competitive mode")
    async def enablecompmode(self, ctx, enabled: bool, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "EnableCompMode", str(enabled))
            await ctx.send(f"Competitive mode has been {'enabled' if enabled else 'disabled'} on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set competitive mode: `{e}`")

    @cmd(name="enablewhitelist", help="Enables or disables the whitelist")
    async def enablewhitelist(self, ctx, enabled: bool, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "EnableWhitelist", str(enabled))
            await ctx.send(f"Whitelist has been {'enabled' if enabled else 'disabled'} on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set whitelist: `{e}`")

    @cmd(name="setlimitedammotype", help="Sets ammo limitation type")
    async def setlimitedammotype(self, ctx, ammo_type: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        if ammo_type < 0 or ammo_type > 5:
            await ctx.send("Ammo type must be between 0 and 5")
            return
        try:
            await send_rcon(server_name, "SetLimitedAmmoType", str(ammo_type))
            await ctx.send(f"Set ammo limitation type to `{ammo_type}` on `{server_name}`")
        except Exception as e:
            await ctx.send(f"Failed to set ammo type: `{e}`")

    @cmd(name="custom", help="Send a raw RCON command")
    async def custom(self, ctx, *, raw_command: str):
        try:
            server_name, command_text = self._resolve_custom_target(raw_command)
        except ValueError as e:
            await ctx.send(f"Failed to run custom command: `{e}`")
            return

    @cmd(name="removemod", help="Removes a player from moderators")
    async def removemod(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return

        try:
            await send_rcon(server_name, command_text, wait_response=False)
            await ctx.send(f"Acknowledged. Sent custom command to `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to run custom command: `{e}`")


async def setup(bot):
    await bot.add_cog(Admin(bot))
