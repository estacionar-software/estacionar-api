from models.ProductOrService import ProductOrService
from utils.products_or_services_helpers import from_db_to_products_or_services

def insert_product_or_service_on_table_products_and_services(cursor, res):
    command = '''
    INSERT INTO products_and_services (id, description, title, amount, price, type, created_at)
    VALUES (%(id)s, %(description)s, %(title)s, %(amount)s, %(price)s, %(type)s, %(created_at)s)
    '''
    cursor.execute(command, res)
    return

def get_product_or_service_on_table_product_and_service(cursor):
    command = '''
    SELECT * FROM products_and_services
    '''
    cursor.execute(command)
    return cursor.fetchall()

def delete_product_or_service_on_table_product_and_service(cursor):
    command = '''
    DELETE FROM products_and_services
    '''
    cursor.execute(command)
    return

def find_product_or_service_by_id(cursor, id: str):
    cursor.execute('SELECT * FROM products_and_services WHERE id = %s', (id,))
    res = cursor.fetchone()
    return from_db_to_products_or_services(res) if res else None
    