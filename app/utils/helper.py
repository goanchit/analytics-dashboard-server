import datetime

def handle_time(from_ts, to_ts):
    if isinstance(from_ts, str):
        from_ts = datetime.datetime.strptime(from_ts,  "%Y-%m-%dT%H:%M:%S.%f%z")
        if from_ts.date() == datetime.datetime.now().date():
            from_ts = datetime.datetime.now(tz=datetime.timezone.utc)
        if from_ts.date() < datetime.datetime.now().date():
            from_ts = from_ts.replace(hour=23, minute=59, second=59)
    
    if isinstance(to_ts, str):
        to_ts =  datetime.datetime.strptime(to_ts,  "%Y-%m-%dT%H:%M:%S.%f%z")
        to_ts = to_ts.replace(hour=0, minute=0, second=0)

    if to_ts > from_ts:
        to_ts = from_ts - datetime.timedelta(days=1)

    return from_ts, to_ts