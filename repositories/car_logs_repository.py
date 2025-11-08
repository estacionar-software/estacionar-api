from utils.car_helpers import from_db_to_car


def total_cars_logs(cursor):
    command = '''SELECT COUNT(*) FROM cars_parked_history'''
    cursor.execute(command)
    total = cursor.fetchone()[0]
    return total

def find_by_plate_on_history(cursor, plate: str):
    cursor.execute('SELECT * FROM cars_parked_history WHERE license_plate = %s', (plate.upper(),))
    res = cursor.fetchone()
    return from_db_to_car(res) if res else None

def list_cars_history(cursor, limit, offset):
    command = '''SELECT * FROM cars_parked_history LIMIT %s OFFSET %s'''
    cursor.execute(command, (limit, offset))
    results = cursor.fetchall()

    return results