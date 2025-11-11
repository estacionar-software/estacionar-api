from utils.car_helpers import from_db_to_car


def total_cars_logs(cursor):
    command = '''SELECT COUNT(*) FROM cars_parked_history'''
    cursor.execute(command)
    total = cursor.fetchone()[0]
    return total

def list_cars_history(cursor, limit, offset, order):
    order = order.upper()

    command = f'''SELECT * FROM cars_parked_history ORDER BY removed_at {order} LIMIT %s OFFSET %s'''
    cursor.execute(command, (limit, offset))
    results = cursor.fetchall()
    return results

def find_by_plate_on_history(cursor, plate: str, limit: int, offset: int, order):
    order  = order.upper()
    command = f'''SELECT * FROM cars_parked_history 
                  WHERE license_plate LIKE %s 
                  ORDER BY removed_at {order} 
                  LIMIT %s OFFSET %s;'''
    like_pattern = f"%{plate.upper()}%"
    cursor.execute(command, (like_pattern, limit, offset))
    results = cursor.fetchall()
    return results if results else []