from repositories.price_repository import list_prices
from db.database import connection

def create_price(id: str, tolerance_time: int, quick_stop_price: int, until_time_price: int, extra_hour_time: int):
    print("id:", id)
    print(f"Tolerância: {tolerance_time} horas")
    print("Preço parada rápida: R$", quick_stop_price)
    print("Preço até horário limite: R$", until_time_price)
    print("Preço estadia acima do tempo limite: R$", extra_hour_time)

    return {"message": "sucesso!"}, 200

def get_price():
    try:
        with connection.cursor() as cursor:
            response = list_prices(cursor)
            if not response:
                return {"message": "Registro não encontrado"}, 404
            return {"message": "Registro encontrado", "prices": response}, 200
    except Exception as ex: # Se houver qualquer erro, retorna aqui.
        connection.rollback()
        return {"mensagem": str(ex), "carro": None}, 400

def update_price(tolerance_time: int, quick_stop_price: int, until_time_price: int, extra_hour_time: int):
    print(f"Tolerância: {tolerance_time} horas")
    print("Preço parada rápida: R$", quick_stop_price)
    print("Preço até horário limite: R$", until_time_price)
    print("Preço estadia acima do tempo limite: R$", extra_hour_time)

    return {"message": "sucesso!"}, 200

def delete_price():
    print("Preço removido!")

    return {"message": "sucesso!"}, 200