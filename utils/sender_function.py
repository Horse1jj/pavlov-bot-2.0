import asyncio
import json
from contextlib import suppress
from pathlib import Path

from pavlov import PavlovRCON
from utils.server_config import resolve_server_name

SERVERS_PATH = Path(__file__).resolve().parents[1] / "servers.json"
DEFAULT_TIMEOUT = 5

with open(SERVERS_PATH, "r", encoding="utf-8") as f:
    SERVERS = json.load(f)


async def send_rcon(server_name: str, command: str, *args):
    server_name = resolve_server_name(server_name, servers=SERVERS)
    server = SERVERS.get(server_name)
    if not server:
        raise ValueError(f"Server '{server_name}' not found in servers.json")

    full_command = f"{command} {' '.join(str(arg) for arg in args)}".strip()
    timeout = float(server.get("timeout", DEFAULT_TIMEOUT))
    rcon = PavlovRCON(server["ip"], int(server["port"]), server["password"], timeout=timeout)

    try:
        return await asyncio.wait_for(rcon.send(full_command), timeout=timeout)
    except asyncio.TimeoutError as exc:
        raise TimeoutError(f"RCON server did not reply within {timeout:g} seconds") from exc
    finally:
        close = getattr(rcon, "close", None)
        if close is not None:
            result = close()
            if asyncio.iscoroutine(result):
                with suppress(Exception):
                    await result
