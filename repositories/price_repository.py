from models.price import Price

def list_prices(cursor):
    cursor.execute('''SELECT * FROM parking_fees''')
    res = cursor.fetchone()

    if res is None:
        return None

    return Price(id=res[0], quick_stop_price=res[1], until_time_price=res[2], extra_hour_price=res[3], quick_stop_limit_minutes=res[4], parking_hours=res[5]).to_dictionary()

def insert_price_on_table_parking_fees(cursor, res):
    command = '''INSERT INTO parking_fees (id, quick_stop_price, until_time_price, extra_hour_price, quick_stop_limit_minutes, parking_hours)
                        VALUES (%(id)s, %(quick_stop_price)s, %(until_time_price)s, %(extra_hour_price)s, %(quick_stop_limit_minutes)s, %(parking_hours)s)
                        '''
    cursor.execute(command, res)
    return

def delete_price_from_table_parking_fees(cursor):
    command = '''DELETE FROM parking_fees;'''
    cursor.execute(command)
    return

