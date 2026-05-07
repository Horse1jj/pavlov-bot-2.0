import discord
from discord.ext import commands
from utils.permissions import is_server_mod, is_server_admin, has_server_permission

from utils.sender_function import send_rcon




class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.command(name="kick", help="Kick a player from the server")
async def kick(self, ctx, server_name: str, unique_id: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Kick", unique_id)
        await ctx.send(f" `{unique_id}` has been kicked from `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to kick player: `{e}`")



@commands.command(name="ban", help="Ban a player from the server")
async def ban(self, ctx, server_name: str, unique_id: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Ban", unique_id)
        await ctx.send(f" `{unique_id}` has been banned from `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to ban player: `{e}`")


@commands.command(name="unban", help="Unban a player from the server")
async def unban(self, ctx, server_name: str, unique_id: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Unban", unique_id)
        await ctx.send(f" `{unique_id}` has been unbanned from `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to unban player: `{e}`")



@commands.command(name="kill", help="Kill a player in the game")
async def kill(self, ctx, server_name: str, unique_id: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Kill", unique_id)
        await ctx.send(f" `{unique_id}` has been killed in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to kill player: `{e}`")



@commands.command(name="slap", help="Slap a player in the game")
async def slap(self, ctx, server_name: str, unique_id: str, damage: int = 10):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Slap", unique_id, str(damage))
        await ctx.send(f" `{unique_id}` has been slapped for `{damage}` damage in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to slap player: `{e}`")


@commands.command(name="switchteam", help="Switch a player to a different team")
async def switchteam(self, ctx, server_name: str, unique_id: str, team_id: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "SwitchTeam", unique_id, str(team_id))
        await ctx.send(f" `{unique_id}` has been switched to team `{team_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to switch player team: `{e}`")

@commands.command(name="teleport", help="Teleport a player to another player")
async def teleport(self, ctx, server_name: str, unique_id: str, target_unique_id: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Teleport", unique_id, target_unique_id)
        await ctx.send(f" `{unique_id}` has been teleported to `{target_unique_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to teleport player: `{e}`")



@commands.command(name="giveitem", help="Give an item to a player")
async def giveitem(self, ctx, server_name: str, unique_id: str, item_id: int, amount: int = 1):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "GiveItem", unique_id, str(item_id), str(amount))
        await ctx.send(f" `{amount}` of item `{item_id}` has been given to `{unique_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to give item to player: `{e}`")


@commands.command(name="givecash", help="Give cash to a player")
async def givecash(self, ctx, server_name: str, unique_id: str, amount: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "GiveCash", unique_id, str(amount))
        await ctx.send(f" `{amount}` cash has been given to `{unique_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to give cash to player: `{e}`")


@commands.command(name="gag", help="Gag a player in voice chat")
async def gag(self, ctx, server_name: str, unique_id: str, gag: bool):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "Gag", unique_id, str(gag))
        action = "gagged" if gag else "ungagged"
        await ctx.send(f" `{unique_id}` has been {action} in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to gag/ungag player: `{e}`")


@commands.command(name="setplayerskin", help="Set a player's skin")
async def setplayerskin(self, ctx, server_name: str, unique_id: str, skin_id: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "SetPlayerSkin", unique_id, str(skin_id))
        await ctx.send(f" `{unique_id}`'s skin has been set to `{skin_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to set player skin: `{e}`")


@commands.command(name="clearemptyvehicles", help="Remove all unoccupied vehicles from the map")
async def clearemptyvehicles(self, ctx, server_name: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "ClearEmptyVehicles")
        await ctx.send(f" All unoccupied vehicles have been removed from `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to remove empty vehicles: `{e}`")


@commands.command(name="inspectplayer", help="Get detailed status of a player")
async def inspectplayer(self, ctx, server_name: str, unique_id: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "InspectPlayer", unique_id)
        await ctx.send(f" Status for `{unique_id}` in `{server_name}`:\n```\n{response}\n```")
    except Exception as e:
        await ctx.send(f"Failed to inspect player: `{e}`")


@commands.command(name="inspectteam", help="Get status of all players on a team")
async def inspectteam(self, ctx, server_name: str, team_id: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "InspectTeam", str(team_id))
        await ctx.send(f" Status for team `{team_id}` in `{server_name}`:\n```\n{response}\n```")
    except Exception as e:
        await ctx.send(f"Failed to inspect team: `{e}`")


# TTT commands


@commands.command(name="tttsetrole", help="Set a player's TTT role")
async def tttsetrole(self, ctx, server_name: str, unique_id: str, role_id: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "TTTSetRole", unique_id, str(role_id))
        await ctx.send(f" `{unique_id}`'s TTT role has been set to `{role_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to set player's TTT role: `{e}`")


@commands.command(name="tttsetkarma", help="Set a player's TTT karma")
async def tttsetkarma(self, ctx, server_name: str, unique_id: str, karma: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "TTTSetKarma", unique_id, str(karma))
        await ctx.send(f" `{unique_id}`'s TTT karma has been set to `{karma}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to set player's TTT karma: `{e}`")


@commands.command(name="tttpausetimer", help="Pause or unpause the TTT timer")
async def tttpausetimer(self, ctx, server_name: str, pause: bool):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "TTTPauseTimer", str(pause))
        action = "paused" if pause else "unpaused"
        await ctx.send(f" The TTT timer has been {action} in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to pause/unpause TTT timer: `{e}`")


@commands.command(name="tttendround", help="End the current TTT round")
async def tttendround(self, ctx, server_name: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "TTTEndRound")
        await ctx.send(f" The current TTT round has been ended in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to end TTT round: `{e}`")



@commands.command(name="tttflushkarma", help="Reset all player karma to 1200")
async def tttflushkarma(self, ctx, server_name: str):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "TTTFlushKarma")
        await ctx.send(f" All player karma has been reset to 1200 in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to flush TTT karma: `{e}`")


@commands.command(name="tttgivecredits", help="Give TTT credits to a player")
async def tttgivecredits(self, ctx, server_name: str, unique_id: str, amount: int):
    if not has_server_permission(ctx, server_name, required="modroles"):
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        response = await send_rcon(server_name, "TTTGiveCredits", unique_id, str(amount))
        await ctx.send(f" `{amount}` TTT credits have been given to `{unique_id}` in `{server_name}`.")
    except Exception as e:
        await ctx.send(f"Failed to give TTT credits to player: `{e}`")




async def setup(bot):
    await bot.add_cog(Mod(bot))