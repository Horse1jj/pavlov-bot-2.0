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

MENU_COMMANDS = [
    ("Kill",          "Kill",         [],         "Kill a player",                   True,  False),
    ("Slap",          "Slap",         ["10"],     "Slap a player for 10 damage",     True,  False),
    ("Give Item",     "GiveItem",     [],         "Give an item to a player",        True,  True),
    ("Give Vehicle",  "GiveItem",     [],         "Give a vehicle to a player",      True,  True),
    ("Switch Team 0", "SwitchTeam",   ["0"],      "Switch player to blue team",      True,  False),
    ("Switch Team 1", "SwitchTeam",   ["1"],      "Switch player to red team",       True,  False),
    ("Godmode",       "Godmode",      ["true"],   "Enable godmode for a player",     True,  False),
    ("Speed Boost",   "SetSpeed",     ["2"],      "Set player speed to 2x",          True,  False),
    ("No Clip",       "SetNoclip",    ["true"],   "Enable noclip for a player",      True,  False),
    ("Rotate Map",    "RotateMap",    [],         "Rotate to the next map",          False, False),
]
# Fields: label, rcon_cmd, extra_args, desc, needs_player, needs_input


class ItemInputModal(Modal):
    def __init__(self, ctx, server_name, player_list, rcon_cmd, label, command_view):
        super().__init__(title=f"Enter {label} Name")
        self.ctx = ctx
        self.server_name = server_name
        self.player_list = player_list
        self.rcon_cmd = rcon_cmd
        self.label = label
        self.command_view = command_view

        placeholder = "e.g. SportsCar" if "Vehicle" in label else "e.g. AK47"
        self.item_input = TextInput(
            label="Name",
            placeholder=placeholder,
            required=True
        )
        self.add_item(self.item_input)

    async def on_submit(self, interaction: discord.Interaction):
        item_name = self.item_input.value.strip()
        await interaction.response.edit_message(
            embed=discord.Embed(
                title=f"{self.label} — Select a Player",
                description=f"Item: `{item_name}` | Server: `{self.server_name}`",
                color=discord.Color.from_rgb(49, 51, 56)
            ),
            view=PlayerSelect(self.ctx, self.server_name, self.player_list, self.rcon_cmd, [item_name], self.label, self.command_view)
        )
class ServerSelect(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx

        options = [
            discord.SelectOption(label=name, value=name)
            for name in SERVERS.keys()
        ]
        select = Select(placeholder="Select a server...", options=options)
        select.callback = self.server_selected
        self.add_item(select)

    async def server_selected(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This menu is not for you.", ephemeral=True)
            return

        server_name = interaction.data["values"][0]

        if not has_server_permission(self.ctx, server_name, required="modroles"):
            await interaction.response.send_message("You do not have permission for this server.", ephemeral=True)
            return

        await interaction.response.defer()

        try:
            response = await send_rcon(server_name, "RefreshList")
            player_list = response.get("PlayerList", []) if isinstance(response, dict) else []
        except Exception as e:
            await interaction.followup.send(f"Failed to fetch players: `{e}`", ephemeral=True)
            return

        await interaction.edit_original_response(
            embed=discord.Embed(
                title=f"Admin Menu — {server_name}",
                description="Select a command to execute.",
                color=discord.Color.from_rgb(49, 51, 56)
            ),
            view=CommandSelect(self.ctx, server_name, player_list)
        )


class CommandSelect(View):
    def __init__(self, ctx, server_name, player_list):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.server_name = server_name
        self.player_list = player_list

        options = [
            discord.SelectOption(label=label, value=str(i), description=desc)
            for i, (label, _, _, desc, _, _) in enumerate(MENU_COMMANDS)
        ]
        select = Select(placeholder="Select a command...", options=options)
        select.callback = self.command_selected
        self.add_item(select)

    async def go_back(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=discord.Embed(
                title=f"Admin Menu — {self.server_name}",
                description="Select a command to execute.",
                color=discord.Color.from_rgb(49, 51, 56)
            ),
            view=self
        )

    async def command_selected(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This menu is not for you.", ephemeral=True)
            return

        index = int(interaction.data["values"][0])
        label, rcon_cmd, extra_args, desc, needs_player, needs_input = MENU_COMMANDS[index]

        if not needs_player:
            await interaction.response.defer()
            try:
                await send_rcon(self.server_name, rcon_cmd, *extra_args)
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="✅ Done",
                        description=f"`{label}` executed on `{self.server_name}`.\n\nSelect another command below.",
                        color=discord.Color.green()
                    ),
                    view=self
                )
            except Exception as e:
                await interaction.followup.send(f"Failed: `{e}`", ephemeral=True)
            return

        if not self.player_list:
            await interaction.response.send_message("No players online.", ephemeral=True)
            return

        if needs_input:
            await interaction.response.send_modal(
                ItemInputModal(self.ctx, self.server_name, self.player_list, rcon_cmd, label, self)
            )
            return

        await interaction.response.edit_message(
            embed=discord.Embed(
                title=f"{label} — Select a Player",
                description=f"Server: `{self.server_name}`",
                color=discord.Color.from_rgb(49, 51, 56)
            ),
            view=PlayerSelect(self.ctx, self.server_name, self.player_list, rcon_cmd, extra_args, label, self)
        )


class PlayerSelect(View):
    def __init__(self, ctx, server_name, player_list, rcon_cmd, extra_args, label, command_view=None):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.server_name = server_name
        self.rcon_cmd = rcon_cmd
        self.extra_args = extra_args
        self.label = label
        self.command_view = command_view

        options = [
            discord.SelectOption(
                label=p.get("Username", "Unknown"),
                value=p.get("UniqueId", p.get("Username", "Unknown"))
            )
            for p in player_list[:25]
        ]
        select = Select(placeholder="Select a player...", options=options)
        select.callback = self.player_selected
        self.add_item(select)

    async def player_selected(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This menu is not for you.", ephemeral=True)
            return

        unique_id = interaction.data["values"][0]

        await interaction.response.defer()

        try:
            await send_rcon(self.server_name, self.rcon_cmd, unique_id, *self.extra_args)
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title="Done",
                    description=f"`{self.label}` executed on `{unique_id}` in `{self.server_name}`.\n\nSelect another command below.",
                    color=discord.Color.green()
                ),
                view=self.command_view
            )
        except Exception as e:
            await interaction.followup.send(f"Failed: `{e}`", ephemeral=True)


class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd(name="menu", help="Opens the admin menu")
    async def menu(self, ctx):
        embed = discord.Embed(
            title="Admin Menu",
            description="Select a server to get started.",
            color=discord.Color.from_rgb(49, 51, 56)
        )
        await ctx.send(embed=embed, view=ServerSelect(ctx))


async def setup(bot):
    await bot.add_cog(Panel(bot))
