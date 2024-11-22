from datetime import datetime, timezone

datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, datetime_format).replace(tzinfo=timezone.utc)
