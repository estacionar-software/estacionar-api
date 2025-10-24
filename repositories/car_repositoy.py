from utils.car_helpers import from_db_to_car

def find_by_plate(cursor, plate: str):
    cursor.execute('SELECT * FROM cars_parked WHERE license_plate = %s', (plate.upper(),))
    res = cursor.fetchone()
    return from_db_to_car(res) if res else None

def list_cars(cursor, limit, offset):
    command = '''SELECT * FROM cars_parked LIMIT %s OFFSET %s'''
    cursor.execute(command, (limit, offset))
    results = cursor.fetchall()

    return results

def total_cars_parked(cursor):
    command = '''SELECT COUNT(*) FROM cars_parked'''
    cursor.execute(command)
    total = cursor.fetchone()[0]

    return total

def remove_car_from_cars_parked(cursor, car_id):
    command = '''DELETE FROM cars_parked WHERE id = %s;'''
    cursor.execute(command, (car_id,))
