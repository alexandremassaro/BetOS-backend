from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get Current UTC datetime"""
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    """Convert datetime to UTC timezone"""
    if dt.tzinfo is None:
        # Assume naive datetime is UTC
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def from_timestamp(timestamp: float) -> datetime:
    """Create UTC datetime from timestamp"""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
