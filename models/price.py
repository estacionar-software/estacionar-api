import uuid

class Price:
    def __init__(self, id = None, quick_stop_price: int = 0, until_time_price: int = 0, extra_hour_price: int = 0, quick_stop_limit_minutes:int = 0, parking_hours: int = 0):
        self.id = id or str(uuid.uuid4())
        self.quick_stop_price = quick_stop_price
        self.until_time_price = until_time_price
        self.extra_hour_price = extra_hour_price
        self.quick_stop_limit_minutes = quick_stop_limit_minutes
        self.parking_hours = parking_hours

    def to_dictionary(self):
        return {
        "id": self.id,
        'quick_stop_price': self.quick_stop_price,
        'until_time_price': self.until_time_price,
        'extra_hour_price': self.extra_hour_price,
        'quick_stop_limit_minutes': self.quick_stop_limit_minutes,
        'parking_hours': self.parking_hours,
    }
