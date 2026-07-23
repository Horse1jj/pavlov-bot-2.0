import json
import discord
import random
from discord.ext import commands
from utils.discord_embeds import send_rcon_response
from utils.permissions import has_server_permission
from utils.sender_function import send_rcon
from utils.server_config import load_servers, resolve_server_name

with open("config.json") as f:
    config = json.load(f)

SERVERS = load_servers()
cmd = commands.hybrid_command if config.get("hybrid") else commands.command


def success_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, color=discord.Color.green())


def error_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, color=discord.Color.red())


def info_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, color=discord.Color.blurple())


def warn_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, color=discord.Color.yellow())


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd(name="kick", help="Kick a player from the server")
    async def kick(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Kick", unique_id)
            await send_rcon_response(ctx, server_name, "Kick", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to kick player: `{e}`"))

    @cmd(name="ban", help="Ban a player from the server")
    async def ban(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Ban", unique_id)
            await send_rcon_response(ctx, server_name, "Ban", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to ban player: `{e}`"))

    @cmd(name="unban", help="Unban a player from the server")
    async def unban(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Unban", unique_id)
            await send_rcon_response(ctx, server_name, "Unban", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to unban player: `{e}`"))

    @cmd(name="kill", help="Kill a player in the game")
    async def kill(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Kill", unique_id)
            await send_rcon_response(ctx, server_name, "Kill", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to kill player: `{e}`"))

    @cmd(name="slap", help="Slap a player in the game")
    async def slap(self, ctx, unique_id: str, server_name: str = None, damage: int = 10):
        if server_name and server_name.isdigit():
            damage = int(server_name)
            server_name = None
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Slap", unique_id, str(damage))
            await send_rcon_response(ctx, server_name, "Slap", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to slap player: `{e}`"))

    @cmd(name="switchteam", help="Switch a player to a different team")
    async def switchteam(self, ctx, unique_id: str, team_id: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "SwitchTeam", unique_id, str(team_id))
            await send_rcon_response(ctx, server_name, "SwitchTeam", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to switch player team: `{e}`"))

    @cmd(name="teleport", help="Teleport a player to another player")
    async def teleport(self, ctx, unique_id: str, target_unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Teleport", unique_id, target_unique_id)
            await send_rcon_response(ctx, server_name, "Teleport", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to teleport player: `{e}`"))

    @cmd(name="giveitem", help="Give an item to a player")
    async def giveitem(self, ctx, unique_id: str, item_id: str, server_name: str = None, amount: int = 1):
        if server_name and server_name.isdigit():
            amount = int(server_name)
            server_name = None
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "GiveItem", unique_id, item_id, str(amount))
            await send_rcon_response(ctx, server_name, "GiveItem", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to give item to player: `{e}`"))

    @cmd(name="givecash", help="Give cash to a player")
    async def givecash(self, ctx, unique_id: str, amount: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "GiveCash", unique_id, str(amount))
            await send_rcon_response(ctx, server_name, "GiveCash", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to give cash to player: `{e}`"))

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
            await ctx.send(embed=warn_embed(
                f"Missing argument: `gag`\nUsage: `{ctx.prefix}{ctx.command.name} <unique_id> [server] <true/false>`"
            ))
            return
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "Gag", unique_id, str(gag))
            await send_rcon_response(ctx, server_name, "Gag", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to gag/ungag player: `{e}`"))

    @cmd(name="setplayerskin", help="Set a player's skin")
    async def setplayerskin(self, ctx, unique_id: str, skin_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "SetPlayerSkin", unique_id, skin_id)
            await send_rcon_response(ctx, server_name, "SetPlayerSkin", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to set player skin: `{e}`"))

    @cmd(name="clearemptyvehicles", help="Remove all unoccupied vehicles from the map")
    async def clearemptyvehicles(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "ClearEmptyVehicles")
            await send_rcon_response(ctx, server_name, "ClearEmptyVehicles", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to remove empty vehicles: `{e}`"))

    @cmd(name="inspectplayer", help="Get detailed status of a player")
    async def inspectplayer(self, ctx, unique_id: str, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "InspectPlayer", unique_id)
            await send_rcon_response(ctx, server_name, "InspectPlayer", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to inspect player: `{e}`"))

    @cmd(name="inspectteam", help="Get status of all players on a team")
    async def inspectteam(self, ctx, team_id: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "InspectTeam", str(team_id))
            await send_rcon_response(ctx, server_name, "InspectTeam", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to inspect team: `{e}`"))

    @cmd(name="inspectall", help="Returns status for all players")
    async def inspectall(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "InspectAll")
            await send_rcon_response(ctx, server_name, "InspectAll", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to inspect all players: `{e}`"))

    @cmd(name="banlist", help="Lists banned players")
    async def banlist(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "BanList")
            await send_rcon_response(ctx, server_name, "BanList", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to get ban list: `{e}`"))

    @cmd(name="itemlist", help="Lists available items")
    async def itemlist(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "ItemList")
            await send_rcon_response(ctx, server_name, "ItemList", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to get item list: `{e}`"))
    

    @cmd(name="flush", help="Kick a random player to free a slot")
    async def flush(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            resp = await send_rcon(server_name, "RefreshList")
            players = resp.get("PlayerList") if isinstance(resp, dict) else []

            if not players:
                await ctx.send(embed=warn_embed(f"No players to kick on `{server_name}`."))
                return

            victim = random.choice(players)
            uid = victim.get("UniqueId")
            name = victim.get("Username", "Unknown")

            if not uid:
                await ctx.send(embed=error_embed("Failed to retrieve a valid UniqueId for the selected player."))
                return

            response = await send_rcon(server_name, "Kick", uid)
            await send_rcon_response(ctx, server_name, "Kick", response)

        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to flush server slot: `{e}`"))


    # ── TTT ───────────────────────────────────────────────────────────────────

    @cmd(name="tttsetrole", help="Set a player's TTT role")
    async def tttsetrole(self, ctx, unique_id: str, role_id: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "TTTSetRole", unique_id, str(role_id))
            await send_rcon_response(ctx, server_name, "TTTSetRole", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to set player's TTT role: `{e}`"))

    @cmd(name="tttsetkarma", help="Set a player's TTT karma")
    async def tttsetkarma(self, ctx, unique_id: str, karma: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "TTTSetKarma", unique_id, str(karma))
            await send_rcon_response(ctx, server_name, "TTTSetKarma", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to set player's TTT karma: `{e}`"))

    @cmd(name="tttpausetimer", help="Pause or unpause the TTT timer")
    async def tttpausetimer(self, ctx, pause: bool, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "TTTPauseTimer", str(pause))
            await send_rcon_response(ctx, server_name, "TTTPauseTimer", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to pause/unpause TTT timer: `{e}`"))

    @cmd(name="tttendround", help="End the current TTT round")
    async def tttendround(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "TTTEndRound")
            await send_rcon_response(ctx, server_name, "TTTEndRound", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to end TTT round: `{e}`"))

    @cmd(name="tttflushkarma", help="Reset all player karma to 1200")
    async def tttflushkarma(self, ctx, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "TTTFlushKarma")
            await send_rcon_response(ctx, server_name, "TTTFlushKarma", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to flush TTT karma: `{e}`"))

    @cmd(name="tttgivecredits", help="Give TTT credits to a player")
    async def tttgivecredits(self, ctx, unique_id: str, amount: int, server_name: str = None):
        server_name = resolve_server_name(server_name, config=config)
        if not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send(embed=error_embed("You do not have permission to use this command."))
            return
        try:
            response = await send_rcon(server_name, "TTTGiveCredits", unique_id, str(amount))
            await send_rcon_response(ctx, server_name, "TTTGiveCredits", response)
        except Exception as e:
            await ctx.send(embed=error_embed(f"Failed to give TTT credits to player: `{e}`"))


async def setup(bot):
    await bot.add_cog(Mod(bot))