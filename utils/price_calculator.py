import datetime
import math
from repositories.price_repository import list_prices

def calculate_price(enter_time, cursor):

    res = list_prices(cursor)

    if res is None:
        time = None
        value = None
        exit_hour = None
        return time, value, exit_hour

    hours_in_seconds = datetime.timedelta(hours=res['parking_hours'])
    hours_in_seconds = hours_in_seconds.total_seconds()

    exit_hour = datetime.datetime.now()
    if isinstance(enter_time, str):
        enter_time = datetime.datetime.fromisoformat(enter_time)

    length_of_stay = exit_hour - enter_time
    total_seconds = int(length_of_stay.total_seconds())
    hours, resto = divmod(total_seconds, 3600)
    minutes, _ = divmod(resto, 60)

    quick_stop_limit_seconds = int(res['quick_stop_limit_minutes']) * 60
    if int(res['quick_stop_limit_minutes']) > 0:
        if total_seconds <= quick_stop_limit_seconds:
            value = res['quick_stop_price']
            time = f"{minutes} minutos"
            return time, value, exit_hour.strftime('%Y-%m-%dT%H:%M:%S')
    elif total_seconds <= hours_in_seconds:
        value = res['until_time_price']
        time = f"{hours}h{minutes:02d}m"
        return time, value, exit_hour.strftime('%Y-%m-%dT%H:%M:%S')

    overtime_in_seconds = total_seconds - hours_in_seconds
    overtime = math.ceil(overtime_in_seconds / 3600)
    total_price = res['until_time_price'] + (overtime * res['extra_hour_price'])
    total_time = f"{hours}h{minutes:02d}m"

    return total_time, total_price, exit_hour.strftime('%Y-%m-%dT%H:%M:%S')
