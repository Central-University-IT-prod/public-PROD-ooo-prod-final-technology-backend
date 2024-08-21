import datetime as dt


def get_utc() -> dt.datetime:
    return dt.datetime.now(tz=dt.timezone.utc).replace(tzinfo=None)


def get_utc_timestamp() -> int:
    return int(get_utc().timestamp())
