import datetime # Biblioteca para horários
import math # Biblioteca para Operações Matematicas
from models.car import Carro # Importando da pasta models do arquivo car, a classe Carro
from database import connection # Importando o conector do banco de dados

def cadastrarCarro(id: str, license_plate: str, model: str): # Função para cadastrar carro novo no banco de dados
    try:
        with connection.cursor() as cursor:
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
            cursor.execute(search_vehicle, (license_plate.upper(),))
            res = cursor.fetchone()

            if res:
                return {"mensagem": "Carro já cadastrado!"}, 400

            parked = True
            novo_carro = Carro(id, license_plate, parked, model)

            insert_car = """
            INSERT INTO cars_parked (id, license_plate, model, parked, created_at)
            VALUES (%(id)s, %(license_plate)s, %(model)s, %(parked)s, %(created_at)s)
            """
            cursor.execute(insert_car, novo_carro.toDictionary())
            connection.commit()

            return {"mensagem": "Carro cadastrado com sucesso!", "carro": novo_carro.toDictionary()}, 201
    except Exception as ex:
        connection.rollback()
        return {"mensagem": str(ex), "carro": None}, 400

def consultarCarros(license_plate: str = None):
    columns = ['id', 'license_plate', 'model', 'parked', 'created_at']

    try:
        with connection.cursor() as cursor:
            if license_plate:
                searchVehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
                cursor.execute(searchVehicle, (license_plate.upper(),))
                res = cursor.fetchone()
                if not res:
                    return {"mensagem": "Carro não encontrado"}, 404

                carro_dict = dict(zip(columns, res))
                return carro_dict, 200

            all_vehicles = '''SELECT * FROM cars_parked'''
            cursor.execute(all_vehicles)
            results = cursor.fetchall()
            cars = [dict(zip(columns, car)) for car in results]

            return cars, 200
    except Exception as ex:
        connection.rollback()
        return {"mensagem": str(ex), "carro": None}, 400

def calculate_price(enter_time: datetime.datetime):
    exit_hour = datetime.datetime.now()
    length_of_stay = exit_hour - enter_time

    total_seconds = int(length_of_stay.total_seconds())
    hours, resto = divmod(total_seconds, 3600)
    minutes, _ = divmod(resto, 60)

    if total_seconds <= 1800:
        return {"valor": 7, "tempo": f"{minutes} minutos"}
    elif total_seconds <= 10800:
        return {"valor": 13, "tempo": f"{hours}h{minutes:02d}m"}

    overtime_in_seconds = total_seconds - 10800
    overtime = math.ceil(overtime_in_seconds / 3600)
    total_price = 13 + (overtime * 2)

    return {"valor": total_price, "tempo": f"{hours}h{minutes:02d}m"}

def removerCarro(placa: str):
    for carro in carrosEstacionados:
        if carro.placa == placa.upper():
            carrosEstacionados.remove(carro)
            valor = calculate_price(carro.horarioEntrada)
            return {"carro": carro.toDictionary(), "pagamento": valor}, 200
    return {"erro": "Carro não encontrado"}, 404

