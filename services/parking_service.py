import datetime # Biblioteca para horários
import uuid

from models.car import Carro # Importando da pasta models do arquivo car, a classe Carro

from db.database import connection # Importando o conector do banco de dados

from repositories.car_repositoy import find_by_plate, list_cars, total_cars_parked, remove_car_from_cars_parked, search_cars_by_plate

from utils.price_calculator import calculate_price
from utils.car_helpers import from_db_to_car

def cadastrarCarro(id: str, license_plate: str, model: str, locale: str): # Função para cadastrar carro novo no banco de dados
    license_plate = license_plate.upper()

    if not license_plate or len(license_plate) < 5:
        return {"message": "Placa inválida"}, 400
    try:
        with connection.cursor() as cursor: # Garante abertura e fechamento seguro do cursor
            res = find_by_plate(cursor, license_plate)

            if res: #se tem resposta
                return {"mensagem": "Carro já cadastrado!"}, 400 # Mensagem de erro

            parked = True # Deixamos parked como True, pois ele passou da verificação então é um registro novo
            novo_carro = Carro(id, license_plate, parked, model, locale) # Instanciamos a classe Carro para novo_carro passando todos os atributos

            insert_car = """ 
            INSERT INTO cars_parked (id, license_plate, model, parked, created_at, locale)
            VALUES (%(id)s, %(license_plate)s, %(model)s, %(parked)s, %(created_at)s, %(locale)s)
            """ # Insert no banco de dados
            cursor.execute(insert_car, novo_carro.toDictionary()) # Executa a mudança no banco de dados
            connection.commit() # Salva a mudança
            print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {novo_carro.modelo} de placa {license_plate} (ID: {novo_carro.id}) adicionado ao sistema.")
            return {"mensagem": "Carro cadastrado com sucesso!", "carro": novo_carro.toDictionary()}, 201 # Mensagem de sucesso
    except Exception as ex: # Se houver qualquer erro, retorna aqui.
        connection.rollback()
        return {"mensagem": str(ex), "carro": None}, 400

def consultarCarros(license_plate: str = None, page: int = 1, limit: int = 10):
    columns = ['id', 'license_plate', 'model', 'parked', 'created_at', 'locale']
    try:
        with connection.cursor() as cursor:
            total = total_cars_parked(cursor)
            if license_plate:
                offset = (page - 1) * limit
                cars = [Carro(id=car[0], placa=car[1], modelo=car[2], parked=car[3], locale=car[5], horario_entrada=car[4]).toDictionary() for car in search_cars_by_plate(cursor, license_plate, limit, offset)]
                if not cars:
                    return {"message": "Carro não encontrado"}, 404

                print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Consulta unitária realizada com sucesso!")
                return {
                "carros": [
                    cars
                ],
                "totalSearch": 1,
                "totalVehicles": total,

                }, 200

            offset = (page -1) * limit
            results = list_cars(cursor, limit, offset)
            cars = [dict(zip(columns, car)) for car in results]
            for car in cars:
                if isinstance(car['created_at'], datetime.datetime):
                    car['created_at'] = car['created_at'].strftime('%Y-%m-%dT%H:%M:%S')

            if not cars:
                return {"message": "Não há carros no sistema"}, 404

            print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Consulta realizada com sucesso!")

            return {
                "pagina": page,
                "limite": limit,
                "totalVehicles": total,
                "totalSearch": total,
                "carros": cars
            }, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "carro": None}, 400


def removerCarro(license_plate: str):
    try:
        with connection.cursor() as cursor:
            car = find_by_plate(cursor, license_plate)
            if not car:
                return {"message": "Carro não encontrado"}, 404



            total_time, total_price, exit_hour = calculate_price(car['created_at'], cursor)
            car.update({
                "total_price": total_price,
                "total_time": total_time,
                "exit_hour": exit_hour
            })

            remove_car_from_cars_parked(cursor, (car['id']))

            car_parked_history = car.copy()

            car_parked_history.update({
                "car_id": car['id'],
                "id": str(uuid.uuid4()),
            })

            insert_car = """ 
                        INSERT INTO cars_parked_history (id, car_id, license_plate, model, locale, parked, created_at, removed_at, price)
                        VALUES (%(id)s, %(car_id)s, %(license_plate)s, %(model)s, %(locale)s, %(parked)s, %(created_at)s, %(exit_hour)s, %(total_price)s)
                        """  # Insert no banco de dados

            cursor.execute(insert_car, car_parked_history)
            connection.commit()
        print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {car['model']} de placa {license_plate} (ID: {car['id']}) removido do sistema ")
        print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ID REGISTRO HISTÓRICO {car_parked_history['id']} | {car_parked_history['model']} de placa {license_plate} (ID: {car_parked_history['car_id']}) arquivado no histórico.")
        return {"message": "Veiculo excluído com sucesso.", "data": car }, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "carro": None}, 400

def update_car(plate, new_license_plate: str, model: str, new_locale: str):

    try:
        with connection.cursor() as cursor:
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
            cursor.execute(search_vehicle, (new_license_plate.upper(),))
            res = cursor.fetchone()

            if res:
                return {"message": "Carro já cadastrado"}, 400

            cursor.execute(search_vehicle, (plate.upper(),))
            res = cursor.fetchone()

            if not res:
                return {"message": "Carro não encontrado"}, 404

            car = from_db_to_car(res)

            if new_license_plate:
                new_license_plate = new_license_plate.upper()

            if new_license_plate and model and new_locale:
                update = """UPDATE cars_parked SET model = %s, locale = %s, license_plate = %s WHERE license_plate = %s"""
                cursor.execute(update, (model, new_locale, new_license_plate, plate))
                connection.commit()
                car.update({
                    "license_plate": new_license_plate.upper(),
                    "model": model,
                    "locale": new_locale
                })

                print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ATUALIZAÇÃO DE MODELO, PLACA E LOCAL NO SISTEMA: (ID: {car['id']})")
                return {"message": "Veiculo atualizado com sucesso.", "carro": car}, 200

            if new_license_plate:
                update = """UPDATE cars_parked SET license_plate = %s WHERE license_plate = %s"""
                cursor.execute(update, (new_license_plate.upper(), plate))

                car.update({
                    "license_plate": new_license_plate.upper(),
                })

            if model:
                update = """UPDATE cars_parked SET model = %s WHERE license_plate = %s"""
                cursor.execute(update, (model, plate))

                car.update({
                    "model": model
                })

            if new_locale:
                update = """UPDATE cars_parked SET locale = %s WHERE license_plate = %s"""
                cursor.execute(update, (new_locale, plate))

                car.update({
                    "locale": new_locale
                })

            connection.commit()
            print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ATUALIZAÇÃO NO SISTEMA: (ID: {car['id']})")
            return {"message": "Veiculo atualizado com sucesso.", "carro": car}, 200
    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "carro": None}, 400