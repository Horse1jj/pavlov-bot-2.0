import json
import shlex
from discord.ext import commands
from utils.permissions import has_server_permission
from utils.sender_function import send_rcon
from utils.server_config import load_servers, resolve_server_name

with open("config.json") as f:
    config = json.load(f)

SERVERS = load_servers()

cmd = commands.hybrid_command if config.get("hybrid") else commands.command


class Mod(commands.Cog):
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

    @cmd(name="kick", help="Kick a player from the server")
    async def kick(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Kick", unique_id)
            await ctx.send(f"`{unique_id}` has been kicked from `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to kick player: `{e}`")

    @cmd(name="ban", help="Ban a player from the server")
    async def ban(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Ban", unique_id)
            await ctx.send(f"`{unique_id}` has been banned from `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to ban player: `{e}`")

    @cmd(name="unban", help="Unban a player from the server")
    async def unban(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Unban", unique_id)
            await ctx.send(f"`{unique_id}` has been unbanned from `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to unban player: `{e}`")

    @cmd(name="kill", help="Kill a player in the game")
    async def kill(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Kill", unique_id)
            await ctx.send(f"`{unique_id}` has been killed in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to kill player: `{e}`")

    @cmd(name="slap", help="Slap a player in the game")
    async def slap(self, ctx, unique_id: str, server_name: str = None, damage: int = 10):
        if server_name and server_name.isdigit():
            damage = int(server_name)
            server_name = None
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Slap", unique_id, str(damage))
            await ctx.send(f"`{unique_id}` has been slapped for `{damage}` damage in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to slap player: `{e}`")

    @cmd(name="switchteam", help="Switch a player to a different team")
    async def switchteam(self, ctx, unique_id: str, team_id: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "SwitchTeam", unique_id, str(team_id))
            await ctx.send(f"`{unique_id}` has been switched to team `{team_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to switch player team: `{e}`")

    @cmd(name="teleport", help="Teleport a player to another player")
    async def teleport(self, ctx, unique_id: str, target_unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Teleport", unique_id, target_unique_id)
            await ctx.send(f"`{unique_id}` has been teleported to `{target_unique_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to teleport player: `{e}`")

    @cmd(name="giveitem", help="Give an item to a player")
    async def giveitem(self, ctx, unique_id: str, item_id: str, server_name: str = None, amount: int = 1):
        if server_name and server_name.isdigit():
            amount = int(server_name)
            server_name = None

        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "GiveItem", unique_id, item_id, str(amount))
            await ctx.send(f"`{amount}` of item `{item_id}` has been given to `{unique_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to give item to player: `{e}`")

    @cmd(name="givecash", help="Give cash to a player")
    async def givecash(self, ctx, unique_id: str, amount: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "GiveCash", unique_id, str(amount))
            await ctx.send(f"`{amount}` cash has been given to `{unique_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to give cash to player: `{e}`")

    @cmd(name="gag", help="Gag a player in voice chat")
    async def gag(self, ctx, unique_id: str, server_name: str = None, gag: bool = None):
        if gag is None and server_name is not None:
            lowered = server_name.lower()
            if lowered in {"true", "yes", "y", "1", "on"}:
                gag = True
                server_name = None
            elif lowered in {"false", "no", "n", "0", "off"}:
                gag = False
                server_name = None

        if gag is None:
            await ctx.send(f"Missing argument: `gag`\nUsage: `{ctx.prefix}{ctx.command.name} <unique_id> [server] <true/false>`")
            return

        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "Gag", unique_id, str(gag))
            action = "gagged" if gag else "ungagged"
            await ctx.send(f"`{unique_id}` has been {action} in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to gag/ungag player: `{e}`")

    @cmd(name="setplayerskin", help="Set a player's skin")
    async def setplayerskin(self, ctx, unique_id: str, skin_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "SetPlayerSkin", unique_id, skin_id)
            await ctx.send(f"`{unique_id}`'s skin has been set to `{skin_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to set player skin: `{e}`")

    @cmd(name="clearemptyvehicles", help="Remove all unoccupied vehicles from the map")
    async def clearemptyvehicles(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "ClearEmptyVehicles")
            await ctx.send(f"All unoccupied vehicles have been removed from `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to remove empty vehicles: `{e}`")

    @cmd(name="inspectplayer", help="Get detailed status of a player")
    async def inspectplayer(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            response = await send_rcon(server_name, "InspectPlayer", unique_id)
            await ctx.send(f"Status for `{unique_id}` in `{server_name}`:\n```\n{response}\n```")
        except Exception as e:
            await ctx.send(f"Failed to inspect player: `{e}`")

    @cmd(name="inspectteam", help="Get status of all players on a team")
    async def inspectteam(self, ctx, team_id: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            response = await send_rcon(server_name, "InspectTeam", str(team_id))
            await ctx.send(f"Status for team `{team_id}` in `{server_name}`:\n```\n{response}\n```")
        except Exception as e:
            await ctx.send(f"Failed to inspect team: `{e}`")

    @cmd(name="custom", help="Send a raw RCON command")
    async def custom(self, ctx, *, raw_command: str):
        try:
            server_name, command_text = self._resolve_custom_target(raw_command)
        except ValueError as e:
            await ctx.send(f"Failed to run custom command: `{e}`")
            return

        if not has_server_permission(ctx, server_name, required="adminroles"):
            await ctx.send("You do not have permission to use this command.")
            return

        try:
            await send_rcon(server_name, command_text, wait_response=False)
            await ctx.send(f"Acknowledged. Sent custom command to `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to run custom command: `{e}`")

    @cmd(name="inspectall", help="Returns status for all players")
    async def inspectall(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "InspectAll", "Player inspection", require_mod=True)

    
    @cmd(name="banlist", help="Lists banned players")
    async def banlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "BanList", "Ban list", require_mod=True)

    @cmd(name="itemlist", help="Lists available items")
    async def itemlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "ItemList", "Item list", require_mod=True)


    # ── TTT ───────────────────────────────────────────────────────────────────

    @cmd(name="tttsetrole", help="Set a player's TTT role")
    async def tttsetrole(self, ctx, unique_id: str, role_id: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "TTTSetRole", unique_id, str(role_id))
            await ctx.send(f"`{unique_id}`'s TTT role has been set to `{role_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to set player's TTT role: `{e}`")

    @cmd(name="tttsetkarma", help="Set a player's TTT karma")
    async def tttsetkarma(self, ctx, unique_id: str, karma: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "TTTSetKarma", unique_id, str(karma))
            await ctx.send(f"`{unique_id}`'s TTT karma has been set to `{karma}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to set player's TTT karma: `{e}`")

    @cmd(name="tttpausetimer", help="Pause or unpause the TTT timer")
    async def tttpausetimer(self, ctx, pause: bool, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "TTTPauseTimer", str(pause))
            action = "paused" if pause else "unpaused"
            await ctx.send(f"The TTT timer has been {action} in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to pause/unpause TTT timer: `{e}`")

    @cmd(name="tttendround", help="End the current TTT round")
    async def tttendround(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "TTTEndRound")
            await ctx.send(f"The current TTT round has been ended in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to end TTT round: `{e}`")

    @cmd(name="tttflushkarma", help="Reset all player karma to 1200")
    async def tttflushkarma(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "TTTFlushKarma")
            await ctx.send(f"All player karma has been reset to 1200 in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to flush TTT karma: `{e}`")

    @cmd(name="tttgivecredits", help="Give TTT credits to a player")
    async def tttgivecredits(self, ctx, unique_id: str, amount: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            await send_rcon(server_name, "TTTGiveCredits", unique_id, str(amount))
            await ctx.send(f"`{amount}` TTT credits have been given to `{unique_id}` in `{server_name}`.")
        except Exception as e:
            await ctx.send(f"Failed to give TTT credits to player: `{e}`")
     

async def setup(bot):
    await bot.add_cog(Mod(bot))
