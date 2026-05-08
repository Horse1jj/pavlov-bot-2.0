import discord
import json
from discord.ext import commands
from discord.ui import View, Select, Modal, TextInput
from utils.sender_function import send_rcon
from utils.permissions import has_server_permission

with open("servers.json") as f:
    SERVERS = json.load(f)

with open("config.json") as f:
    config = json.load(f)



cmd = commands.hybrid_command if config.get("hybrid") else commands.command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




@cmd(name="switchmap", description="Immediately switches to a map")
@has_server_permission()
async def switchmap(self, ctx, map_id: str, game_mode: str):
    await send_rcon(ctx.guild.id, f"switchmap {map_id} {game_mode}")
    await ctx.send(f"Switched to map `{map_id}` with game mode `{game_mode}`")


@cmd(name="maplist", description="Returns the current map rotation")
@has_server_permission()
async def maplist(self, ctx):
    response = await send_rcon(ctx.guild.id, "maplist")
    await ctx.send(f"Current map rotation:\n```\n{response}\n```")



@cmd(name="addmaprotation", description="Adds a map to the rotation")
@has_server_permission()
async def addmaprotation(self, ctx, map_id: str, game_mode: str):
    await send_rcon(ctx.guild.id, f"addmaprotation {map_id} {game_mode}")
    await ctx.send(f"Added map `{map_id}` with game mode `{game_mode}` to the rotation")


@cmd(name="removemaprotation", description="Removes a map from the rotation")
@has_server_permission()
async def removemaprotation(self, ctx, map_id: str, game_mode: str):
    await send_rcon(ctx.guild.id, f"removemaprotation {map_id} {game_mode}")
    await ctx.send(f"Removed map `{map_id}` with game mode `{game_mode}` from the rotation")


@cmd(name="setmaxplayers", description="Sets the server slot count (1-24)")
@has_server_permission()
async def setmaxplayers(self, ctx, amount: int):
    if amount < 1 or amount > 24:
        await ctx.send("Player count must be between 1 and 24")
        return
    await send_rcon(ctx.guild.id, f"setmaxplayers {amount}")
    await ctx.send(f"Set maximum players to `{amount}`")

@cmd(name="updateservername", description="Changes the server name")
@has_server_permission()
async def updateservername(self, ctx, *, name: str):
    await send_rcon(ctx.guild.id, f"updateservername {name}")
    await ctx.send(f"Updated server name to `{name}`")


@cmd(name="shutdownserver", description="Immediately shuts down the server")
@has_server_permission()
async def shutdownserver(self, ctx):
    await send_rcon(ctx.guild.id, "shutdownserver")
    await ctx.send("Server is shutting down...")


@cmd(name="pausematch", description="Pauses the match for a set amount of seconds")
@has_server_permission()
async def pausematch(self, ctx, seconds: int):
    await send_rcon(ctx.guild.id, f"pausematch {seconds}")
    await ctx.send(f"Paused match for `{seconds}` seconds")


@cmd(name="resetsnd", description="Resets the current SND match")
@has_server_permission()
async def resetsnd(self, ctx):
    await send_rcon(ctx.guild.id, "resetsnd")
    await ctx.send("SND match has been reset")


@cmd(name="setpin", description="Sets or removes the server join pin")
@has_server_permission()
async def setpin(self, ctx, pin_number: str):
    if pin_number.lower() == "none":
        await send_rcon(ctx.guild.id, "setpin none")
        await ctx.send("Server join pin has been removed")
    else:
        await send_rcon(ctx.guild.id, f"setpin {pin_number}")
        await ctx.send(f"Server join pin has been set to `{pin_number}`")



@cmd(name="settimelimit", description="Sets the match time limit")
@has_server_permission()
async def settimelimit(self, ctx, seconds: int):
    await send_rcon(ctx.guild.id, f"settimelimit {seconds}")
    await ctx.send(f"Match time limit has been set to `{seconds}` seconds")


@cmd(name="shownametags", description="Enables or disables friendly nametags")
@has_server_permission()
async def shownametags(self, ctx, enabled: bool):
    await send_rcon(ctx.guild.id, f"shownametags {enabled}")
    await ctx.send(f"Friendly nametags have been {'enabled' if enabled else 'disabled'}")


@cmd(name="enablecompmode", description="Enables or disables competitive mode")
@has_server_permission()
async def enablecompmode(self, ctx, enabled: bool):
    await send_rcon(ctx.guild.id, f"enablecompmode {enabled}")
    await ctx.send(f"Competitive mode has been {'enabled' if enabled else 'disabled'}")


@cmd(name="enablewhitelist", description="Enables or disables the whitelist")
@has_server_permission()
async def enablewhitelist(self, ctx, enabled: bool):
    await send_rcon(ctx.guild.id, f"enablewhitelist {enabled}")
    await ctx.send(f"Whitelist has been {'enabled' if enabled else 'disabled'}")


@cmd(name="setlimitedammotype", description="Sets ammo limitation type")
@has_server_permission()
async def setlimitedammotype(self, ctx, ammo_type: int):
    if ammo_type < 0 or ammo_type > 5:
        await ctx.send("Ammo type must be between 0 and 5")
        return
    await send_rcon(ctx.guild.id, f"setlimitedammotype {ammo_type}")
    await ctx.send(f"Set ammo limitation type to `{ammo_type}`")


@cmd(name="addmod", description="Adds a player as server moderator")
@has_server_permission()
async def addmod(self, ctx, unique_id: str):
    await send_rcon(f"addmod {unique_id}")
    await ctx.send(f"Player with ID `{unique_id}` has been added as a moderator")


@cmd(name="removemod", description="Removes a player from moderators")
@has_server_permission()
async def removemod(self, ctx, unique_id: str):
    await send_rcon(f"removemod {unique_id}")
    await ctx.send(f"Player with ID `{unique_id}` has been removed from moderators")



async def setup(bot):
    await bot.add_cog(Admin(bot))