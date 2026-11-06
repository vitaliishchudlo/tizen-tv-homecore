"""CLI: python -m tizen_tv_homecore <command>"""
import argparse
import warnings

warnings.filterwarnings("ignore")


def main() -> None:
    ap = argparse.ArgumentParser(prog="tizen-homecore")
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("pair", help="Перше підключення до ТВ (підтвердити запит на екрані)")

    p = sub.add_parser("key", help="Надіслати клавіші пульта, напр. KEY_MUTE")
    p.add_argument("keys", nargs="+")

    p = sub.add_parser("play", help="Увімкнути відео на YouTube")
    p.add_argument("video", nargs="?", default=None, help="ID відео або посилання")

    p = sub.add_parser("brightness", help="Змінити яскравість через меню (від'ємне = темніше)")
    p.add_argument("steps", type=int)
    p.add_argument("--item", type=int, default=0)

    sub.add_parser("modes", help="Показати режими зображення")

    p = sub.add_parser("chill", help="Сценарій chill")
    p.add_argument("seconds", nargs="?", type=float, default=20)
    p.add_argument("video", nargs="?", default=None)

    a = ap.parse_args()

    from . import chill, smartthings, tv, youtube

    if a.command == "pair":
        print("Дивись на екран ТВ: натисни 'Дозволити' на пульті")
        print(tv.remote().rest_device_info()["device"]["PowerState"])
    elif a.command == "key":
        tv.send_keys(*a.keys)
    elif a.command == "play":
        youtube.play(a.video or youtube.DEFAULT_VIDEO)
    elif a.command == "brightness":
        tv.adjust_expert_setting(a.steps, a.item)
    elif a.command == "modes":
        st = smartthings.status()["custom.picturemode"]
        print("Поточний:", st["pictureMode"]["value"])
        print("Доступні:", st["supportedPictureModes"]["value"])
    elif a.command == "chill":
        chill.run(a.seconds, a.video or youtube.DEFAULT_VIDEO)


if __name__ == "__main__":
    main()
