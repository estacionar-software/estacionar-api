from db.database import connection
from models.ProductOrService import ProductOrService
from repositories.products_and_services_repository import insert_product_or_service_on_table_products_and_services, get_product_or_service_on_table_product_and_service, delete_product_or_service_on_table_product_and_service, find_product_or_service_by_id

def create_product_or_service(description = str, title = str, amount = int, price = int, type = str):
    try:
        with connection.cursor() as cursor:
            product = ProductOrService(description=description, title=title, amount=amount, price=price, type=type).to_dictionary()
            insert_product_or_service_on_table_products_and_services(cursor, product)
            connection.commit()            
            return {"message": "Produto ou serviço adicionado ao sistema!"}, 200

    except Exception as e:
        connection.rollback()
        return {"message": str(e)}, 400

def get_product_or_service():
    try:
        with connection.cursor() as cursor:
            response = get_product_or_service_on_table_product_and_service(cursor)
            products = [
                ProductOrService(
                    id=product[0],
                    title=product[1],
                    description=product[2],
                    amount=product[3],
                    price=product[4],
                    type=product[5],
                    created_at=product[6]).to_dictionary() for product in response]
            return {"message": "Sucesso!", "products": products}, 200
        
    except Exception as e:
        connection.rollback()
        return {"message": str(e)}, 400
    

def update_product_or_service(description: str = None, title: str = None, amount: int = None, price: int = None, type: str = None):
    try:
        with connection.cursor() as cursor:
            print("teste")
    except Exception as e:
        connection.rollback()
        return {"message": str(e)}, 400

def delete_product_or_service(id):
    try:
        with connection.cursor() as cursor:
            response = find_product_or_service_by_id(cursor, id)
            if not response:
                return {"message": "Não há nada a ser deletado"}, 404
            delete_product_or_service_on_table_product_and_service(cursor)
            connection.commit()
            return {"message": "Sucesso, registro apagado!"}, 200

    except Exception as e:
        connection.rollback()
        return {"message": str(e)}, 400
    

