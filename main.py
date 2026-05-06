import discord
from discord.ext import commands
from pavlov import PavlovRCON
from dotenv import load_dotenv
import asyncio
import os
from colorama import Fore, Style
import platform
import json

with open("config.json") as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())


def print_banner():
    ascii_art = Fore.RED + """
    ██████╗  █████╗ ██╗   ██╗██╗      ██████╗ ██╗   ██╗
    ██╔══██╗██╔══██╗██║   ██║██║     ██╔═══██╗██║   ██║
    ██████╔╝███████║██║   ██║██║     ██║   ██║██║   ██║
    ██╔═══╝ ██╔══██║╚██╗ ██╔╝██║     ██║   ██║╚██╗ ██╔╝
    ██║     ██║  ██║ ╚████╔╝ ███████╗╚██████╔╝ ╚████╔╝ 
    ╚═╝     ╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝   ╚═══╝  
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
    print(Fore.GREEN + f"  Logged in as {bot.user}" + Style.RESET_ALL)
    print(Fore.RED  + f"  Cogs loaded:  " + Style.RESET_ALL + ", ".join(bot.cogs.keys()))

async def main():
    async with bot:
        await load_cogs()
        print("Bot loading!")
        await bot.start(config["token"])

asyncio.run(main())