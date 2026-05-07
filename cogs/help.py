import discord
import json
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

cmd = commands.hybrid_command if config.get("hybrid") else commands.command

PAVLOV_COMMANDS = {
    "Player": [
        ("kick", "[UniqueID]", "Kicks a player from the server"),
        ("ban", "[UniqueID]", "Kicks and permanently bans a player"),
        ("unban", "[UniqueID]", "Unbans a player"),
        ("kill", "[UniqueID]", "Kills a player"),
        ("slap", "[UniqueID] [Amount]", "Deals damage to a player"),
        ("switchteam", "[UniqueID] [TeamID]", "Moves a player to a team (0=blue, 1=red)"),
        ("gag", "[UniqueID] [True/False]", "Gags or ungags a player's voice chat"),
        ("teleport", "[SourceID] [TargetID]", "Teleports source player to target player"),
        ("setplayerskin", "[UniqueID] [SkinID]", "Sets a player's skin"),
        ("givecash", "[UniqueID] [Amount]", "Gives cash to a player"),
        ("setcash", "[UniqueID] [Amount]", "Sets a player's cash (0-16000)"),
        ("giveitem", "[UniqueID] [ItemID]", "Gives an item to a player"),
        ("inspectplayer", "[UniqueID]", "Returns detailed status for a player"),
    ],
    "Server": [
        ("serverinfo", "none", "Returns server info (map, mode, score, players)"),
        ("refreshlist", "none", "Lists all connected players and their UniqueIDs"),
        ("inspectall", "none", "Returns status for all players"),
        ("rotateMap", "none", "Rotates to the next map in the rotation"),
        ("switchmap", "[MapID] [GameMode]", "Immediately switches to a map"),
        ("maplist", "none", "Returns the current map rotation"),
        ("addmaprotation", "[MapID] [GameMode]", "Adds a map to the rotation"),
        ("removemaprotation", "[MapID] [GameMode]", "Removes a map from the rotation"),
        ("setmaxplayers", "[Amount]", "Sets the server slot count (1-24)"),
        ("updateservername", "[Name]", "Changes the server name"),
        ("shutdownserver", "none", "Immediately shuts down the server"),
        ("pausematch", "[Seconds]", "Pauses the match for a set amount of seconds"),
        ("resetsnd", "none", "Resets the current SND match"),
        ("setpin", "[PinNumber]", "Sets or removes the server join pin"),
        ("settimelimit", "[Seconds]", "Sets the match time limit"),
        ("shownametags", "[True/False]", "Enables or disables friendly nametags"),
        ("enablecompmode", "[True/False]", "Enables or disables competitive mode"),
        ("enablewhitelist", "[True/False]", "Enables or disables the whitelist"),
        ("setlimitedammotype", "[0-5]", "Sets ammo limitation type"),
    ],
    "Moderation": [
        ("addmod", "[UniqueID]", "Adds a player as server moderator"),
        ("removemod", "[UniqueID]", "Removes a player from moderators"),
        ("moderatorlist", "none", "Lists all moderators"),
        ("banlist", "none", "Lists all banned players"),
        ("giveall", "[TeamID] [ItemID]", "Gives an item to all players on a team"),
        ("giveteamcash", "[TeamID] [Amount]", "Gives cash to all players on a team"),
        ("clearemptyvehicles", "none", "Removes all unoccupied vehicles"),
        ("inspectteam", "[TeamID]", "Returns status for all players on a team"),
        ("itemlist", "none", "Lists all available items"),
    ],
    "TTT": [
        ("tttendround", "[TeamID]", "Ends the current TTT round"),
        ("tttflushkarma", "none", "Resets all player karma to 1200"),
        ("tttgivecredits", "[UniqueID] [Amount]", "Gives TTT credits to a player"),
        ("tttsetrole", "[UniqueID] [RoleID]", "Sets a player's TTT role"),
        ("tttsetkarma", "[UniqueID] [Amount]", "Sets a player's TTT karma"),
        ("tttpausetimer", "[True/False]", "Pauses the TTT timer"),
    ],
    "Public": [
        ("players", "[Servername]", "Shows all players on the selected server"),
        ("ping", "", "Shows the bots ping"),
    ],
}

MAX_CHARS = 5500


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @cmd()
    async def help(self, ctx):
        prefix = await self.bot.get_prefix(ctx)
        if isinstance(prefix, list):
            prefix = prefix[0]

        chunks = []
        current_chunk = ""

        for category, cmds in PAVLOV_COMMANDS.items():
            section = f"\n**{category}**\n"

            for name, params, desc in cmds:
                line = f"`{prefix}{name} {params}` — {desc}\n"

                if len(current_chunk) + len(section) + len(line) > MAX_CHARS:
                    chunks.append(current_chunk)
                    current_chunk = section + line
                    section = ""
                else:
                    section += line

            section += "\n"
            current_chunk += section

        if current_chunk:
            chunks.append(current_chunk)

        for i, chunk in enumerate(chunks, start=1):
            embed = discord.Embed(
                title="Commands",
                description=chunk,
                color=discord.Color.dark_grey()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))