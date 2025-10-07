import datetime # Biblioteca para horários
import math # Biblioteca para Operações Matematicas
from models.car import Carro # Importando da pasta models do arquivo car, a classe Carro
from database import connection # Importando o conector do banco de dados

def cadastrarCarro(id: str, license_plate: str, model: str): # Função para cadastrar carro novo no banco de dados
    try:
        with connection.cursor() as cursor: # Garante abertura e fechamento seguro do cursor
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s''' # Consulta sql, seleciona todos na table cars_parked onde license_plate seja igual ao license_plate digitado pelo user
            cursor.execute(search_vehicle, (license_plate.upper(),)) # Executa a consulta sql passando a consulta de search_vehicle e a license plate que quero verificar
            res = cursor.fetchone() # Retorna uma resposta

            if res: #se tem resposta
                return {"mensagem": "Carro já cadastrado!"}, 400 # Mensagem de erro

            parked = True # Deixamos parked como True, pois ele passou da verificação então é um registro novo
            novo_carro = Carro(id, license_plate, parked, model) # Instanciamos a classe Carro para novo_carro passando todos os atributos

            insert_car = """ 
            INSERT INTO cars_parked (id, license_plate, model, parked, created_at)
            VALUES (%(id)s, %(license_plate)s, %(model)s, %(parked)s, %(created_at)s)
            """ # Insert no banco de dados
            cursor.execute(insert_car, novo_carro.toDictionary()) # Executa a mudança no banco de dados
            connection.commit() # Salva a mudança

            return {"mensagem": "Carro cadastrado com sucesso!", "carro": novo_carro.toDictionary()}, 201 # Mensagem de sucesso
    except Exception as ex: # Se houver qualquer erro, retorna aqui.
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

