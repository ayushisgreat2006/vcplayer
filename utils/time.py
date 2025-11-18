# utils/time.py
def seconds_to_time(sec: int) -> str:
    if sec is None: return "N/A"
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
