"""Локальне керування ТВ: WebSocket-пульт, статус, UPnP-гучність."""
import re
import time
import urllib.request

from samsungtvws import SamsungTVWS

from . import config


def remote() -> SamsungTVWS:
    return SamsungTVWS(host=config.TV_HOST, port=8002,
                       token_file=config.TV_TOKEN_FILE, name=config.TV_APP_NAME)


def is_on() -> bool:
    try:
        url = f"http://{config.TV_HOST}:8001/api/v2/"
        return '"PowerState":"on"' in urllib.request.urlopen(url, timeout=3).read().decode()
    except Exception:
        return False


def send_keys(*keys: str, delay: float = 0.7) -> None:
    tv = remote()
    for k in keys:
        tv.send_key(k, cmd="Click")
        time.sleep(delay)


def live_volume() -> int:
    """Гучність напряму з ТВ по UPnP (SmartThings віддає її із затримкою)."""
    body = ('<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
            's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>'
            '<u:GetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">'
            '<InstanceID>0</InstanceID><Channel>Master</Channel></u:GetVolume></s:Body></s:Envelope>')
    req = urllib.request.Request(
        f"http://{config.TV_HOST}:9197/upnp/control/RenderingControl1", data=body.encode(),
        headers={"Content-Type": 'text/xml; charset="utf-8"',
                 "SOAPACTION": '"urn:schemas-upnp-org:service:RenderingControl:1#GetVolume"'})
    return int(re.search(r"<CurrentVolume>(\d+)", urllib.request.urlopen(req, timeout=5).read().decode()).group(1))


def adjust_expert_setting(steps: int, item: int = 0) -> None:
    """Змінює пункт Експертних налаштувань зображення емуляцією пульта.
    steps<0 - темніше/менше, steps>0 - світліше/більше. item=0 - перший пункт (яскравість).
    KEY_EXIT не використовуємо - він виходить з YouTube."""
    send_keys("KEY_MENU", delay=1.2)
    send_keys("KEY_UP", "KEY_UP", "KEY_UP", "KEY_ENTER", "KEY_DOWN", "KEY_DOWN", "KEY_ENTER", delay=0.8)
    send_keys(*(["KEY_DOWN"] * item), "KEY_ENTER", delay=0.6)
    send_keys(*(["KEY_RIGHT" if steps > 0 else "KEY_LEFT"] * abs(steps)), delay=0.25)
