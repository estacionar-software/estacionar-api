import datetime
import math
from repositories.price_repository import list_prices

def calculate_price(enter_time, cursor):

    res = list_prices(cursor)
    hours_in_seconds = datetime.timedelta(hours=res['tolerance_time'])
    hours_in_seconds = hours_in_seconds.total_seconds()

    exit_hour = datetime.datetime.now()
    if isinstance(enter_time, str):
        enter_time = datetime.datetime.fromisoformat(enter_time)

    length_of_stay = exit_hour - enter_time
    total_seconds = int(length_of_stay.total_seconds())
    hours, resto = divmod(total_seconds, 3600)
    minutes, _ = divmod(resto, 60)

    if total_seconds <= 1800:
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
