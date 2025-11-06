from db.database import connection
from models.ProductOrService import ProductOrService
from repositories.products_and_services_repository import insert_product_or_service_on_table_products_and_services

def create_product_or_service(id = int, description = str, title = str, amount = int, price = int, type = str):
    try:
        with connection.cursor() as cursor:
            product = ProductOrService(description=description, title=title, amount=amount, price=price, type=type).to_dictionary()
            insert_product_or_service_on_table_products_and_services(cursor, product)
            connection.commit()            
            return {"message": "Produto ou serviço adicionado ao sistema!"}, 200

    except Exception as e:
        connection.rollback()
        return {"message": str(e)}, 400
