from models.price import Price
from repositories.price_repository import list_prices, insert_price_on_table_parking_fees, delete_price_from_table_parking_fees
from db.database import connection

def create_price( parking_hours: int, quick_stop_price: int, until_time_price: int, extra_hour_price: int, quick_stop_limit_minutes: int):
    try:
        with connection.cursor() as cursor:

            have_price = list_prices(cursor)

            if have_price:
                return {"message": "Já possui um preço no sistema, não é possível incluir outro!"}, 403

            prices = Price(quick_stop_price=quick_stop_price, until_time_price=until_time_price, extra_hour_price=extra_hour_price, quick_stop_limit_minutes=quick_stop_limit_minutes, parking_hours=parking_hours).to_dictionary()

            insert_price_on_table_parking_fees(cursor, prices)
            connection.commit()

            return {"message": "Preços adicionado ao sistema!"}, 201
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

def update_price(parking_hours: int = None, quick_stop_limit_minutes: int = None, quick_stop_price: int = None, until_time_price: int = None, extra_hour_price: int = None):
    try:
        with connection.cursor() as cursor:
            record_id = list_prices(cursor).pop('id')
            if not record_id:
                return {"message": "ID não fornecido"}, 400
            # Campos que podem ser atualizados
            fields = {
                "parking_hours": parking_hours,
                "quick_stop_price": quick_stop_price,
                "until_time_price": until_time_price,
                "extra_hour_price": extra_hour_price,
                "quick_stop_limit_minutes": quick_stop_limit_minutes,
            }
            # Monta os campos que não são None
            set_clauses = []
            values = []
            for key, value in fields.items():
                if value is not None:
                    set_clauses.append(f"{key} = %s")
                    values.append(value)

            if not set_clauses:
                return {"message": "Nenhum campo para atualizar"}, 400

            values.append(record_id)  # para o WHERE
            sql = f"UPDATE parking_fees SET {', '.join(set_clauses)} WHERE id = %s"
            cursor.execute(sql, values)
            connection.commit()

            # Retorna os dados atualizados (opcional, só para feedback)
            updated_prices = {key: value for key, value in fields.items() if value is not None}
            return {"message": "Preços atualizados com sucesso", "prices": updated_prices}, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "prices": None},  400

    return {"message": "sucesso!"}, 200

def delete_price():
    try:
        with connection.cursor() as cursor:
            response = list_prices(cursor)
            if not response:
                return {"message": "Não há preços para serem excluidos!"}, 404

            delete_price_from_table_parking_fees(cursor)
            connection.commit()
            return {"message": "Sucesso, registro apagado!"}, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex)}, 400