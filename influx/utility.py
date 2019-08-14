import time
import datetime
import pytz

def _current_time_stamp():
    return int(round(time.time() * 1000))

def _utc_timestamp(timestamp):
    utc = pytz.utc
    d = datetime.datetime.fromtimestamp(int(round(timestamp/1000))).replace(tzinfo=utc)
    return d.isoformat()
