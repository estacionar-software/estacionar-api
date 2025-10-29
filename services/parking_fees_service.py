from models.price import Price
from repositories.price_repository import list_prices, insert_price_on_table_parking_fees
from db.database import connection

def create_price( tolerance_time: int, quick_stop_price: int, until_time_price: int, extra_hour_price: int):
    try:
        with connection.cursor() as cursor:

            have_price = list_prices(cursor)

            if have_price:
                return {"message": "Já possui um preço no sistema, não é possível incluir outro!"}, 401

            prices = Price(quick_stop_price=quick_stop_price, until_time_price=until_time_price, extra_hour_price=extra_hour_price, tolerance_time=tolerance_time).to_dictionary()

            insert_price_on_table_parking_fees(cursor, prices)
            connection.commit()

            return {"message": "Preços adicionado ao sistema!"}, 200
    except Exception as e:
        connection.rollback()
        return {"message": str(e)}, 400

def get_price():
    try:
        with connection.cursor() as cursor:
            response = list_prices(cursor)
            if not response:
                return {"message": "Registro não encontrado"}, 404
            return {"message": "Registro encontrado", "prices": response}, 200
    except Exception as ex: # Se houver qualquer erro, retorna aqui.
        connection.rollback()
        return {"mensagem": str(ex), "prices": None}, 400

def update_price(tolerance_time: int, quick_stop_price: int, until_time_price: int, extra_hour_time: int):
    print(f"Tolerância: {tolerance_time} horas")
    print("Preço parada rápida: R$", quick_stop_price)
    print("Preço até horário limite: R$", until_time_price)
    print("Preço estadia acima do tempo limite: R$", extra_hour_time)

    return {"message": "sucesso!"}, 200

def delete_price():
    print("Preço removido!")

    return {"message": "sucesso!"}, 200