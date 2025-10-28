from models.price import Price

def list_prices(cursor):
    cursor.execute('''SELECT * FROM parking_fees''')
    res = cursor.fetchone()
    return Price(res[0], res[1], res[2], res[3], res[4]).to_dictionary()