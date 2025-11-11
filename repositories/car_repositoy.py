from utils.car_helpers import from_db_to_car

def find_by_plate(cursor, plate: str):
    cursor.execute('SELECT * FROM cars_parked WHERE license_plate = %s', (plate.upper(),))
    res = cursor.fetchone()
    return from_db_to_car(res) if res else None

def total_cars_parked(cursor):
    command = '''SELECT COUNT(*) FROM cars_parked'''
    cursor.execute(command)
    total = cursor.fetchone()[0]

    return total

def remove_car_from_cars_parked(cursor, car_id):
    command = '''DELETE FROM cars_parked WHERE id = %s;'''
    cursor.execute(command, (car_id,))

def list_cars(cursor, limit, offset, order: str):
    order = order.upper()

    command = f'''SELECT * FROM cars_parked ORDER BY created_at {order} LIMIT %s OFFSET %s'''
    cursor.execute(command, (limit, offset))
    results = cursor.fetchall()
    return results


def search_cars_by_plate(cursor, plate: str, limit: int, offset: int, order: str):
    order = order.upper()
    command = f'''SELECT * FROM cars_parked 
                  WHERE license_plate LIKE %s 
                  ORDER BY created_at {order} 
                  LIMIT %s OFFSET %s;'''
    like_pattern = f"%{plate.upper()}%"
    cursor.execute(command, (like_pattern, limit, offset))
    results = cursor.fetchall()
    return results if results else []