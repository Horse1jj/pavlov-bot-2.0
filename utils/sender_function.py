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


