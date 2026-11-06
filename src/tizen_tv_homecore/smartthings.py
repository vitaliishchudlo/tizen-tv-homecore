"""SmartThings API: режими зображення, гучність, живлення."""
import json
import urllib.request

from . import config

API = "https://api.smartthings.com/v1/devices/"


def _api(path: str, body: dict | None = None) -> dict:
    if not config.SMARTTHINGS_DEVICE_ID:
        raise RuntimeError("Не задано SMARTTHINGS_DEVICE_ID")
    with open(config.SMARTTHINGS_TOKEN_FILE, encoding="utf-8") as f:
        token = f.read().strip()
    req = urllib.request.Request(
        API + config.SMARTTHINGS_DEVICE_ID + path,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))


def command(capability: str, cmd: str, args: list | None = None) -> dict:
    return _api("/commands", {"commands": [
        {"component": "main", "capability": capability, "command": cmd, "arguments": args or []}
    ]})


def status() -> dict:
    return _api("/status")["components"]["main"]


def picture_modes() -> list[str]:
    return status()["custom.picturemode"]["supportedPictureModes"]["value"]


def set_picture_mode(mode: str) -> dict:
    return command("custom.picturemode", "setPictureMode", [mode])


def set_volume(level: int) -> dict:
    return command("audioVolume", "setVolume", [level])


def power_off() -> dict:
    return command("switch", "off")
