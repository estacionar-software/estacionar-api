from models.car import Carro

def from_db_to_car(res):
    return Carro(
        id=res[0],
        placa=res[1],
        parked=res[3],
        modelo=res[2],
        horario_entrada=res[4],
        locale=res[5],
    ).toDictionary()