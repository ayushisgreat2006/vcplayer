def format_duration(seconds: int) -> str:
    """Convert seconds to MM:SS format"""
    if not seconds or seconds < 0:
        return "0:00"
    
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

def parse_seek_time(time_str: str) -> int:
    """Parse seek time from string (e.g., 1:30 -> 90)"""
    try:
        if ":" in time_str:
            parts = time_str.split(":")
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes * 60 + seconds
        return int(time_str)
    except:
        return 0

def generate_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Generate a progress bar string"""
    if not total or total <= 0:
        return "▱" * length
    
    filled = int(length * current / total)
    bar = "▰" * filled + "▱" * (length - filled)
    return bar
