from datetime import datetime

datetime_format = "%Y-%m-%dT%H:%M:%S.%f"


def parse_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, datetime_format)
