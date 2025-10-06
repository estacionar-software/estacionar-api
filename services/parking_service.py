import datetime
import math
from models.car import Carro

from database import cursor, connection

def cadastrarCarro(id: str, license_plate: str, model: str):
    try:
        searchVehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
        cursor.execute(searchVehicle, (license_plate.upper(),))
        res = cursor.fetchone()

        if res:
            return {"mensagem": "Carro já cadastrado!"}, 400

        parked = True
        novo_carro = Carro(id, license_plate, parked, model)

        insertCar = """
        INSERT INTO cars_parked (id, license_plate, model, parked, created_at)
        VALUES (%(id)s, %(license_plate)s, %(model)s, %(parked)s, %(created_at)s)
        """
        cursor.execute(insertCar, novo_carro.toDictionary())
        connection.commit()

        return {"mensagem": "Carro cadastrado com sucesso!", "carro": novo_carro.toDictionary()}, 201
    except Exception as ex:
        connection.rollback()
        return {"mensagem": str(ex), "carro": None}, 400

def consultarCarros(license_plate: str = None):
    if license_plate:
        searchVehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
        cursor.execute(searchVehicle, (license_plate.upper(),))
        res = cursor.fetchone()
        if res:
            columns = ['id', 'license_plate', 'model', 'parked', 'created_at']
            carro_dict = dict(zip(columns, res))
            return carro_dict, 200

        return {"erro": "Carro não encontrado"}, 404

    all_vehicles = '''SELECT * FROM cars_parked'''
    cursor.execute(all_vehicles)
    carros = cursor.fetchall()
    columns = ['id', 'license_plate', 'model', 'parked', 'created_at']
    return [dict(zip(columns, c)) for c in carros], 200

def calcularValor(horarioEntrada: datetime.datetime):
    horaSaida = datetime.datetime.now()
    tempoPermanencia = horaSaida - horarioEntrada

    totalSegundos = int(tempoPermanencia.total_seconds())
    horas, resto = divmod(totalSegundos, 3600)
    minutos, _ = divmod(resto, 60)

    if totalSegundos <= 1800:
        return {"valor": 7, "tempo": f"{minutos} minutos"}
    elif totalSegundos <= 10800:
        return {"valor": 13, "tempo": f"{horas}h{minutos:02d}m"}

    horasExtrasSegundos = totalSegundos - 10800
    horasExtras = math.ceil(horasExtrasSegundos / 3600)
    valorFinal = 13 + (horasExtras * 2)

    return {"valor": valorFinal, "tempo": f"{horas}h{minutos:02d}m"}


def removerCarro(placa: str):
    for carro in carrosEstacionados:
        if carro.placa == placa.upper():
            carrosEstacionados.remove(carro)
            valor = calcularValor(carro.horarioEntrada)
            return {"carro": carro.toDictionary(), "pagamento": valor}, 200
    return {"erro": "Carro não encontrado"}, 404

