import json
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_PATH / "config.json"
SERVERS_PATH = ROOT_PATH / "servers.json"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_servers() -> dict:
    with open(SERVERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_default_server(config: dict | None = None, servers: dict | None = None) -> str:
    config = config or load_config()
    servers = servers or load_servers()
    default_server = config.get("default_server")

    if not default_server:
        raise ValueError("No default_server is set in config.json")

    if default_server not in servers:
        raise ValueError(
            f"Default server '{default_server}' does not exist in servers.json. "
            f"Available servers: {', '.join(servers.keys())}"
        )

    return default_server


def resolve_server_name(server_name: str | None, config: dict | None = None, servers: dict | None = None) -> str:
    if server_name:
        return server_name
    return get_default_server(config=config, servers=servers)


def ensure_default_server(config: dict | None = None, servers: dict | None = None) -> str:
    return get_default_server(config=config, servers=servers)
