from datetime import datetime

def log_with_time(message: str) -> str:
    return f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}: {message}"
