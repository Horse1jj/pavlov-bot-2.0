import json
from pathlib import Path
from typing import Iterable

from discord import Member
from discord.ext.commands import Context
from utils.server_config import resolve_server_name

SERVERS_PATH = Path(__file__).resolve().parents[1] / "servers.json"

with open(SERVERS_PATH, "r", encoding="utf-8") as f:
    SERVERS = json.load(f)


def _member_has_role_ids(member: Member, role_ids: Iterable[int]) -> bool:
    if not member or not hasattr(member, "roles"):
        return False

    allowed_ids = {int(rid) for rid in role_ids if isinstance(rid, (int, str)) and str(rid).isdigit()}
    return any(role.id in allowed_ids for role in member.roles)


def get_server_role_ids(server_name: str, role_key: str) -> list[int]:
    server_name = resolve_server_name(server_name, servers=SERVERS)
    server = SERVERS.get(server_name)
    if not server:
        raise ValueError(f"Server '{server_name}' not found in servers.json")

    return server.get(role_key, []) if isinstance(server.get(role_key, []), list) else []


def is_server_mod(member: Member, server_name: str) -> bool:
    """Return True if the member has any of the modroles configured for the server."""
    mod_roles = get_server_role_ids(server_name, "modroles")
    return _member_has_role_ids(member, mod_roles)


def is_server_admin(member: Member, server_name: str) -> bool:
    """Return True if the member has any of the adminroles configured for the server."""
    admin_roles = get_server_role_ids(server_name, "adminroles")
    return _member_has_role_ids(member, admin_roles)


def has_server_permission(ctx: Context, server_name: str, required: str = "modroles") -> bool:
    """Check whether the invoking user has the required configured role for a server."""
    if ctx.guild is None:
        return False

    if required not in {"modroles", "adminroles"}:
        raise ValueError("required must be 'modroles' or 'adminroles'")

    return _member_has_role_ids(ctx.author, get_server_role_ids(server_name, required))
