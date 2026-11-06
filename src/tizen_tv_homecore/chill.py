"""Сценарій CHILL: YouTube -> темний режим + тиха гучність -> відлік -> норма -> вимкнення ТВ."""
import time

from . import smartthings as st, tv, youtube

CHILL_IDX = 2     # "Натурал." - режим з мінімальною яскравістю
NORMAL_IDX = 4    # "Фільм" - нормальний режим
CHILL_VOLUME = 5
LEAD = 3          # за скільки секунд до кінця повертаємо норму


def retry(fn, tries: int = 10, delay: float = 2):
    for i in range(tries):
        try:
            return fn()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(delay)


def run(seconds: float = 20, video: str = youtube.DEFAULT_VIDEO) -> None:
    if not tv.is_on():
        raise SystemExit("ТВ вимкнений - увімкни його і запусти знову")

    normal_vol = retry(tv.live_volume)
    modes = retry(st.picture_modes)

    youtube.play(video)
    time.sleep(3)  # дати відео стартувати

    retry(lambda: st.set_picture_mode(modes[CHILL_IDX]))
    retry(lambda: st.set_volume(CHILL_VOLUME))
    t0 = time.time()
    print(f"Chill: темний режим, гучність {CHILL_VOLUME}, відлік {seconds} с")

    time.sleep(max(0, seconds - (time.time() - t0) - LEAD))
    retry(lambda: st.set_picture_mode(modes[NORMAL_IDX]))
    retry(lambda: st.set_volume(normal_vol))
    print("Відновлено:", modes[NORMAL_IDX], normal_vol)
    time.sleep(LEAD)
    st.power_off()
    print("ТВ вимкнено")
