import datetime # Biblioteca para horários
import uuid

from models.vehicle import Vehicle # Importando da pasta models do arquivo car, a classe Carro

from db.database import connection # Importando o conector do banco de dados

from repositories.car_repositoy import find_by_plate, list_cars, total_cars_parked, remove_car_from_cars_parked, search_cars_by_plate

from utils.price_calculator import calculate_price
from utils.car_helpers import from_db_to_car

def post_vehicle(id: str, license_plate: str, model: str, locale: str): # Função para cadastrar veiculo novo no banco de dados
    license_plate = license_plate.upper()

    if not license_plate or len(license_plate) < 5:
        return {"message": "Placa inválida"}, 400
    try:
        with connection.cursor() as cursor: # Garante abertura e fechamento seguro do cursor
            res = find_by_plate(cursor, license_plate)

            if res: #se tem resposta
                return {"message": "Veiculo já cadastrado!"}, 400 # Mensagem de erro

            parked = True # Deixamos parked como True, pois ele passou da verificação então é um registro novo
            new_vehicle = Vehicle(id, license_plate, parked, model, locale) # Instanciamos a classe Carro para novo_carro passando todos os atributos

            insert_vehicle = """ 
            INSERT INTO cars_parked (id, license_plate, model, parked, created_at, locale)
            VALUES (%(id)s, %(license_plate)s, %(model)s, %(parked)s, %(created_at)s, %(locale)s)
            """ # Insert no banco de dados
            cursor.execute(insert_vehicle, new_vehicle.toDictionary()) # Executa a mudança no banco de dados
            connection.commit() # Salva a mudança
            print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {new_vehicle.modelo} de placa {license_plate} (ID: {new_vehicle.id}) adicionado ao sistema.")
            return {"message": "Veiculo cadastrado com sucesso!", "vehicle": new_vehicle.toDictionary()}, 201 # Mensagem de sucesso
    except Exception as ex: # Se houver qualquer erro, retorna aqui.
        connection.rollback()
        return {"message": str(ex), "vehicle": None}, 400

def read_vehicles(order: str, license_plate: str = None, page: int = 1, limit: int = 10):
    columns = ['id', 'license_plate', 'model', 'parked', 'created_at', 'locale']
    try:
        with connection.cursor() as cursor:
            total = total_cars_parked(cursor)
            offset = (page - 1) * limit

            if license_plate:
                vehicles = [
                    Vehicle(
                        id=vehicle[0],
                        placa=vehicle[1],
                        modelo=vehicle[2],
                        parked=vehicle[3],
                        locale=vehicle[5],
                        horario_entrada=vehicle[4]
                    ).toDictionary()
                    for vehicle in search_cars_by_plate(cursor, license_plate, limit, offset, order)
                ]

                if not vehicles:
                    return {"message": "Veiculos não encontrado"}, 404

                print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Consulta unitária realizada com sucesso!")
                return {
                    "vehicles": vehicles,
                    "totalSearch": len(vehicles),
                    "totalVehicles": total,
                    "order": order.upper()
                }, 200

            results = list_cars(cursor, limit, offset, order)
            vehicles = [dict(zip(columns, car)) for car in results]

            for vehicle in vehicles:
                if isinstance(vehicle['created_at'], datetime.datetime):
                    vehicle['created_at'] = vehicle['created_at'].strftime('%Y-%m-%dT%H:%M:%S')

            if not vehicles:
                return {"message": "Não há carros no sistema"}, 404

            print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Consulta realizada com sucesso!")

            return {
                "page": page,
                "limit": limit,
                "totalVehicles": total,
                "totalSearch": total,
                "order": order.upper(),
                "vehicles": vehicles,
            }, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "vehicle": None}, 400


def remove_vehicle(license_plate: str):
    try:
        with connection.cursor() as cursor:
            vehicle = find_by_plate(cursor, license_plate)
            if not vehicle:
                return {"message": "Veiculo não encontrado"}, 404

            total_time, total_price, exit_hour = calculate_price(vehicle['created_at'], cursor)

            if total_time is None and total_price is None and exit_hour is None:
                return {"message": "Não há preços cadastrados!"}, 400

            vehicle.update({
                "total_price": total_price,
                "total_time": total_time,
                "exit_hour": exit_hour
            })

            remove_car_from_cars_parked(cursor, (vehicle['id']))

            vehicle_parked_history = vehicle.copy()

            vehicle_parked_history.update({
                "car_id": vehicle['id'],
                "id": str(uuid.uuid4()),
            })
            insert_vehicle = """ 
                        INSERT INTO cars_parked_history (id, car_id, license_plate, model, locale, parked, created_at, removed_at, price)
                        VALUES (%(id)s, %(car_id)s, %(license_plate)s, %(model)s, %(locale)s, %(parked)s, %(created_at)s, %(exit_hour)s, %(total_price)s)
                        """


            cursor.execute(insert_vehicle, vehicle_parked_history)
            connection.commit()
        print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {vehicle['model']} de placa {license_plate} (ID: {vehicle['id']}) removido do sistema ")
        print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ID REGISTRO HISTÓRICO {vehicle_parked_history['id']} | {vehicle_parked_history['model']} de placa {license_plate} (ID: {vehicle_parked_history['car_id']}) arquivado no histórico.")
        return {"message": "Veiculo excluído com sucesso.", "data": vehicle }, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "vehicle": None}, 400

def update_vehicle(plate, new_license_plate: str, model: str, new_locale: str):

    try:
        with connection.cursor() as cursor:
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
            cursor.execute(search_vehicle, (new_license_plate.upper(),))
            res = cursor.fetchone()

            if res:
                return {"message": "Veiculo já cadastrado"}, 400

            cursor.execute(search_vehicle, (plate.upper(),))
            res = cursor.fetchone()

            if not res:
                return {"message": "Veiculo não encontrado"}, 404

            vehicle = from_db_to_car(res)

            if new_license_plate:
                new_license_plate = new_license_plate.upper()

            if new_license_plate and model and new_locale:
                update = """UPDATE cars_parked SET model = %s, locale = %s, license_plate = %s WHERE license_plate = %s"""
                cursor.execute(update, (model, new_locale, new_license_plate, plate))
                connection.commit()
                vehicle.update({
                    "license_plate": new_license_plate.upper(),
                    "model": model,
                    "locale": new_locale
                })

                print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ATUALIZAÇÃO DE MODELO, PLACA E LOCAL NO SISTEMA: (ID: {vehicle['id']})")
                return {"message": "Veiculo atualizado com sucesso.", "carro": vehicle}, 200

            if new_license_plate:
                update = """UPDATE cars_parked SET license_plate = %s WHERE license_plate = %s"""
                cursor.execute(update, (new_license_plate.upper(), plate))

                vehicle.update({
                    "license_plate": new_license_plate.upper(),
                })

            if model:
                update = """UPDATE cars_parked SET model = %s WHERE license_plate = %s"""
                cursor.execute(update, (model, plate))

                vehicle.update({
                    "model": model
                })

            if new_locale:
                update = """UPDATE cars_parked SET locale = %s WHERE license_plate = %s"""
                cursor.execute(update, (new_locale, plate))

                vehicle.update({
                    "locale": new_locale
                })

            connection.commit()
            print(f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ATUALIZAÇÃO NO SISTEMA: (ID: {vehicle['id']})")
            return {"message": "Veiculo atualizado com sucesso.", "carro": vehicle}, 200
    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "vehicle": None}, 400