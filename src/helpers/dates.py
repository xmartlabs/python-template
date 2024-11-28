from datetime import datetime, timezone

datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_datetime(date_str: str) -> datetime:
    dt = datetime.strptime(date_str, datetime_format)
    return dt.replace(tzinfo=timezone.utc)
