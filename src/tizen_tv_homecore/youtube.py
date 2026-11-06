"""Запуск YouTube на ТВ (DIAL) і керування відтворенням (YouTube Lounge)."""
import asyncio
import re
import time
import urllib.request
from urllib.parse import parse_qs, urlparse

from pyytlounge import YtLoungeApi

from . import config, tv

DEFAULT_VIDEO = "YiDhEkZXCX8"


def parse_video(arg: str) -> tuple[str, str | None, int]:
    """ID відео або повне посилання -> (video_id, playlist_id, start_seconds)."""
    if "http" not in arg:
        return arg, None, 0
    q = parse_qs(urlparse(arg).query)
    start = int(re.sub(r"\D", "", q.get("t", ["0"])[0]) or 0)
    return q["v"][0], q.get("list", [None])[0], start


def dial_screen_id() -> str | None:
    try:
        url = f"http://{config.TV_HOST}:8080/ws/apps/YouTube"
        m = re.search(r"<screenId>([^<]+)", urllib.request.urlopen(url, timeout=5).read().decode())
        return m.group(1) if m else None
    except Exception:
        return None


def launch(timeout: int = 40) -> str:
    """Запускає YouTube на ТВ і повертає screenId."""
    tv.remote().run_app(config.YOUTUBE_APP_ID)
    time.sleep(2)
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"http://{config.TV_HOST}:8001/api/v2/applications/{config.YOUTUBE_APP_ID}",
            method="POST"), timeout=5)
    except Exception:
        pass
    for _ in range(timeout):
        sid = dial_screen_id()
        if sid:
            return sid
        time.sleep(1)
    raise RuntimeError("YouTube не запустився")


async def _play(screen_id: str, video: str, list_id: str | None, start: int) -> None:
    async with YtLoungeApi(config.TV_APP_NAME) as api:
        await api.pair_with_screen_id(screen_id)
        await api.connect()
        await asyncio.sleep(2)
        params: dict = {"videoId": video}
        if list_id:
            params["listId"] = list_id
        if start:
            params["currentTime"] = start
        await api._command("setPlaylist", params)


def play(video_arg: str = DEFAULT_VIDEO) -> None:
    video, list_id, start = parse_video(video_arg)
    asyncio.run(_play(dial_screen_id() or launch(), video, list_id, start))
