import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
import platform
import json
import sys

from utils.server_config import CONFIG_PATH, SERVERS_PATH, ensure_default_server

try:
    from colorama import Fore, Style
except ImportError:
    class _NoColor:
        BLACK = ""
        CYAN = ""
        GREEN = ""
        LIGHTGREEN_EX = ""
        LIGHTMAGENTA_EX = ""
        LIGHTYELLOW_EX = ""
        RED = ""
        WHITE = ""

    Fore = _NoColor()
    Style = type("_NoStyle", (), {"RESET_ALL": ""})()

with open("config.json") as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())


def validate_default_server():
    with open(SERVERS_PATH, "r", encoding="utf-8") as f:
        servers = json.load(f)

    try:
        ensure_default_server(config=config, servers=servers)
        return
    except ValueError as e:
        print(Fore.RED + f"Default server config error: {e}" + Style.RESET_ALL)

    if not sys.stdin.isatty():
        raise SystemExit("Set config.json default_server to one of: " + ", ".join(servers.keys()))

    while True:
        selected = input(f"Choose a default server ({', '.join(servers.keys())}): ").strip()
        if selected in servers:
            config["default_server"] = selected
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
                f.write("\n")
            print(Fore.GREEN + f"Default server set to '{selected}'." + Style.RESET_ALL)
            return

        print(Fore.RED + "That server does not exist in servers.json." + Style.RESET_ALL)


def print_banner():
    ascii_art = Fore.RED + """
    ██████╗  █████╗ ██╗   ██╗██╗      ██████╗ ██╗   ██╗    ██████╗  ██████╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██║   ██║██║     ██╔═══██╗██║   ██║    ██╔══██╗██╔════╝██╔═══██╗████╗  ██║
    ██████╔╝███████║██║   ██║██║     ██║   ██║██║   ██║    ██████╔╝██║     ██║   ██║██╔██╗ ██║
    ██╔═══╝ ██╔══██║╚██╗ ██╔╝██║     ██║   ██║╚██╗ ██╔╝    ██╔══██╗██║     ██║   ██║██║╚██╗██║
    ██║     ██║  ██║ ╚████╔╝ ███████╗╚██████╔╝ ╚████╔╝     ██║  ██║╚██████╗╚██████╔╝██║ ╚████║
    ╚═╝     ╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝   ╚═══╝      ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ (Remote Console Protocol) 
    """ + Style.RESET_ALL

    info = [
        (Fore.LIGHTGREEN_EX + "  Bot"        + Style.RESET_ALL, "Pavlov RCON Bot"),
        (Fore.CYAN + "  Prefix"     + Style.RESET_ALL, config["prefix"]),
        (Fore.LIGHTMAGENTA_EX + "  Python"     + Style.RESET_ALL, platform.python_version()),
        (Fore.BLACK + "  OS"         + Style.RESET_ALL, platform.system()),
        (Fore.LIGHTYELLOW_EX + "  discord.py" + Style.RESET_ALL, discord.__version__),
    ]

    print(ascii_art)
    for label, value in info:
        print(f"  {label}: {Fore.WHITE}{value}{Style.RESET_ALL}")
    print()

load_dotenv()

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

@bot.event
async def on_ready():
    print_banner()
    print(Fore.GREEN + f"  Bot Loaded" + Style.RESET_ALL)
    print(Fore.RED  + f"  Cogs loaded:  " + Style.RESET_ALL + ", ".join(bot.cogs.keys()))

async def main():
    validate_default_server()
    async with bot:
        await load_cogs()
        print("Bot loading!")
        await bot.start(config["token"])

if __name__ == "__main__":
    asyncio.run(main())
