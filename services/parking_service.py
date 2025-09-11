import datetime
import math
from models.car import Carro

# "banco de dados" na memória
carrosEstacionados = []

def cadastrarCarro(placa: str, cor: str, modelo: str):
    for carro in carrosEstacionados:
        if carro.placa == placa.upper():
            return {"erro": "Carro já cadastrado!"}, 400

    novo_carro = Carro(placa, cor, modelo)
    carrosEstacionados.append(novo_carro)
    return {"mensagem": "Carro cadastrado com sucesso!", "carro": novo_carro.toDictionary()}, 201

def consultarCarros(placa: str = None):
    if placa:
        for carro in carrosEstacionados:
            if carro.placa == placa.upper():
                return carro.toDictionary(), 200
        return {"erro": "Carro não encontrado"}, 404

    return [carro.toDictionary() for carro in carrosEstacionados], 200

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

