def insert_product_or_service_on_table_products_and_services(cursor, res):
    command = '''
    INSERT INTO products_and_services (id, description, title, unity, price, type, created_at)
    VALUES (%(id)s, %(description)s, %(title)s, %(unity)s, %(price)s, %(type)s, %(created_at)s)
    '''
    cursor.execute(command, res)
    return