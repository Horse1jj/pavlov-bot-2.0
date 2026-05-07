import discord
from discord.ext import commands
import time
import json
from utils.sender_function import send_rcon

with open("servers.json") as f:
    SERVERS = json.load(f)


class Civilian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Shows all players on a server")
    async def players(self, ctx, server_name: str = None):
        if server_name is None:
            server_list = "\n".join(f"`{s}`" for s in SERVERS.keys())
            embed = discord.Embed(
                title="Select a Server",
                description=f"Please provide a server name:\n{server_list}\n\nUsage: `;players <server>`",
                color=discord.Color.dark_grey()
            )
            await ctx.send(embed=embed)
            return

        if server_name not in SERVERS:
            await ctx.send(f"Server `{server_name}` not found. Use `;players` to see available servers.")
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

    @commands.command(help="Check the bot's response time")
    async def ping(self, ctx):
        start = time.monotonic()
        msg = await ctx.send("Pinging...")
        end = time.monotonic()

        latency = round(self.bot.latency * 1000)
        response_time = round((end - start) * 1000)

        await msg.edit(content=f"Pong! Latency: `{latency}ms` | Response: `{response_time}ms`")


async def setup(bot):
    await bot.add_cog(Civilian(bot))