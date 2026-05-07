import json
from discord.ext import commands
from colorama import Fore, Style

with open("config.json") as f:
    config = json.load(f)


class HybridSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if config.get("hybrid", False):
            await self.bot.tree.sync()
            print(Fore.GREEN + "  Hybrid True: Slash commands synced globally." + Style.RESET_ALL)
        else:
            self.bot.tree.clear_commands(guild=None)
            await self.bot.tree.sync()
            print(Fore.RED + "  Hybrid False: Slash commands cleared." + Style.RESET_ALL)


async def setup(bot):
    await bot.add_cog(HybridSync(bot))