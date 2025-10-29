from models.price import Price

def list_prices(cursor):
    cursor.execute('''SELECT * FROM parking_fees''')
    res = cursor.fetchone()

    if not res:
        return None

    return Price(res[0], res[1], res[2], res[3], res[4]).to_dictionary()

def insert_price_on_table_parking_fees(cursor, res):
    command = '''INSERT INTO parking_fees (id, quick_stop_price, until_time_price, extra_hour_price, tolerance_time)
                        VALUES (%(id)s, %(quick_stop_price)s, %(until_time_price)s, %(extra_hour_price)s, %(tolerance_time)s)
                        '''
    cursor.execute(command, res)
    return

def delete_price_from_table_parking_fees(cursor):
    command = '''DELETE FROM parking_fees;'''
    cursor.execute(command)
    return

