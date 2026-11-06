"""Конфіг з env / .env (без зовнішніх залежностей)."""
import os
from pathlib import Path


def _load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()


def _get(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if val is None:
        raise RuntimeError(f"Не задано змінну {name} (див. .env.example)")
    return val


TV_HOST = _get("TV_HOST", "192.168.0.190")
TV_APP_NAME = _get("TV_APP_NAME", "HomeCore")
TV_TOKEN_FILE = _get("TV_TOKEN_FILE", "token.txt")

SMARTTHINGS_DEVICE_ID = os.environ.get("SMARTTHINGS_DEVICE_ID")
SMARTTHINGS_TOKEN_FILE = _get("SMARTTHINGS_TOKEN_FILE", "smartthings_token.txt")

YOUTUBE_APP_ID = "111299001912"
