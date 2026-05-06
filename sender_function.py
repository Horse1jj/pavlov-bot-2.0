import json
from pavlov import PavlovRCON

with open("servers.json") as f:
    SERVERS = json.load(f)


async def send_rcon(server_name: str, command: str, *args):
    server = SERVERS.get(server_name)
    if not server:
        raise ValueError(f"Server '{server_name}' not found in servers.json")

    rcon = PavlovRCON(
        ip=server["ip"],
        port=server["port"],
        password=server["password"]
    )

    await rcon.open()
    try:
        response = await rcon.send(command, *args)
    finally:
        await rcon.close()

    return response


def has_access(server_name: str, user_id: int, role_ids: list[int]) -> bool:
    """
    Checks if a user has access to run commands on a server.
    Returns True if their user ID or any of their roles are whitelisted.

    :param server_name: Key from servers.json
    :param user_id: Discord user ID
    :param role_ids: List of the user's Discord role IDs
    """
    server = SERVERS.get(server_name)
    if not server:
        return False

    if user_id in server.get("admins", []):
        return True

    if any(role in server.get("roles", []) for role in role_ids):
        return True

    return False