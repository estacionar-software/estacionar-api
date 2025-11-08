import datetime
from models.ProductOrService import ProductOrService

def from_db_to_products_or_services(res):
    #garante que o campo created_at (res[4]) seja datetime, não string
    created_at = res[4]
    if isinstance(created_at, str):
        try:
            #tenta converter se vier em string do banco
            created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            #caso venha com milissegundos
            created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

    product_or_service = ProductOrService(
       id=res[0],title=res[1],
       description=res[2],
       amount=res[3],
       price=res[4],
       type=res[5],
       created_at=res[6])

    return product_or_service.to_dictionary()