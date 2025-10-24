import datetime
import math

def calculate_price(enter_time):
    exit_hour = datetime.datetime.now()
    if isinstance(enter_time, str):
        enter_time = datetime.datetime.fromisoformat(enter_time)

    length_of_stay = exit_hour - enter_time
    total_seconds = int(length_of_stay.total_seconds())
    hours, resto = divmod(total_seconds, 3600)
    minutes, _ = divmod(resto, 60)

    if total_seconds <= 1800:
        value = 7
        time = f"{minutes} minutos"
        return time, value, exit_hour.strftime('%Y-%m-%dT%H:%M:%S')
    elif total_seconds <= 10800:
        value = 13
        time = f"{hours}h{minutes:02d}m"
        return time, value, exit_hour.strftime('%Y-%m-%dT%H:%M:%S')

    overtime_in_seconds = total_seconds - 10800
    overtime = math.ceil(overtime_in_seconds / 3600)
    total_price = 13 + (overtime * 2)
    total_time = f"{hours}h{minutes:02d}m"

    return total_time, total_price, exit_hour.strftime('%Y-%m-%dT%H:%M:%S')
