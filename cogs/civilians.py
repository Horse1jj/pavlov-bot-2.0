import discord
from discord.ext import commands
import time
import json

from utils.sender_function import send_rcon
from utils.permissions import has_server_permission
from utils.server_config import resolve_server_name

with open("servers.json") as f:
    SERVERS = json.load(f)

with open("config.json") as f:
    config = json.load(f)

cmd = commands.hybrid_command if config.get("hybrid") else commands.command


class Civilian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _server_list_text(self):
        return "\n".join(f"`{s}`" for s in SERVERS.keys())

    async def _send_server_picker(self, ctx, command_name: str):
        embed = discord.Embed(
            title="Select a Server",
            description=(
                f"Please provide a server name:\n{self._server_list_text()}\n\n"
                f"Usage: `{ctx.prefix}{command_name} <server>`"
            ),
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)

    async def _send_rcon_output(self, ctx, server_name: str, command: str, title: str, require_mod: bool = False):
        try:
            server_name = resolve_server_name(server_name, config=config, servers=SERVERS)
        except ValueError as e:
            await ctx.send(str(e))
            return

        if server_name not in SERVERS:
            await ctx.send(f"Server `{server_name}` not found. Use `{ctx.prefix}players` to see available servers.")
            return

        if require_mod and not has_server_permission(ctx, server_name, required="modroles"):
            await ctx.send("You do not have permission to use this command.")
            return

        try:
            response = await send_rcon(server_name, command)
        except Exception as e:
            await ctx.send(f"Failed to run `{command}` on `{server_name}`: `{e}`")
            return

        output = json.dumps(response, indent=2) if isinstance(response, (dict, list)) else str(response)
        if len(output) > 1900:
            output = output[:1900] + "\n... truncated"

        await ctx.send(f"{title} for `{server_name}`:\n```json\n{output}\n```")

    @cmd(help="Shows all players on a server")
    async def players(self, ctx, server_name: str = None):
        try:
            server_name = resolve_server_name(server_name, config=config, servers=SERVERS)
        except ValueError as e:
            await ctx.send(str(e))
            return

        if server_name not in SERVERS:
            await ctx.send(f"Server `{server_name}` not found. Use `{ctx.prefix}players` to see available servers.")
            return

        try:
            response = await send_rcon(server_name, "RefreshList")
        except Exception as e:
            await ctx.send(f"Failed to connect to `{server_name}`: `{e}`")
            return

        player_list = response.get("PlayerList", []) if isinstance(response, dict) else []

        embed = discord.Embed(
            title=f"Players on {server_name}",
            color=discord.Color.from_rgb(49, 51, 56)
        )

        if not player_list:
            embed.description = "No players currently online."
        else:
            players_text = "\n\n".join(f"`{p.get('Username', 'Unknown')}`" for p in player_list)
            embed.description = players_text
            embed.set_footer(text=f"Total players: {len(player_list)}")

        await ctx.send(embed=embed)

    @cmd(name="serverinfo", help="Returns server info")
    async def serverinfo(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "ServerInfo", "Server info")

    @cmd(name="refreshlist", help="Lists all connected players and UniqueIDs")
    async def refreshlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "RefreshList", "Player list")

    @cmd(name="inspectall", help="Returns status for all players")
    async def inspectall(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "InspectAll", "Player inspection", require_mod=True)

    @cmd(name="rotatemap", aliases=["rotateMap"], help="Rotates to the next map")
    async def rotatemap(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "RotateMap", "Rotate map result", require_mod=True)

    @cmd(name="moderatorlist", help="Lists server moderators")
    async def moderatorlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "ModeratorList", "Moderator list", require_mod=True)

    @cmd(name="banlist", help="Lists banned players")
    async def banlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "BanList", "Ban list", require_mod=True)

    @cmd(name="itemlist", help="Lists available items")
    async def itemlist(self, ctx, server_name: str = None):
        await self._send_rcon_output(ctx, server_name, "ItemList", "Item list", require_mod=True)

    @cmd(help="Check the bot's response time")
    async def ping(self, ctx):
        start = time.monotonic()
        msg = await ctx.send("Pinging...")
        end = time.monotonic()

        latency = round(self.bot.latency * 1000)
        response_time = round((end - start) * 1000)

        await msg.edit(content=f"Pong! Latency: `{latency}ms` | Response: `{response_time}ms`")


async def setup(bot):
    await bot.add_cog(Civilian(bot))
