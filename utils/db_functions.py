from utils.car_helpers import from_db_to_car


def get_car_by_plate(cursor, plate: str):
    cursor.execute('SELECT * FROM cars_parked WHERE license_plate = %s', (plate.upper(),))
    res = cursor.fetchone()
    return from_db_to_car(res) if res else None