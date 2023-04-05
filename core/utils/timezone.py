from datetime import datetime, timezone, timedelta


def kst_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=9)))
