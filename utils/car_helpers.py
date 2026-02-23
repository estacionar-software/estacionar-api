from models.vehicle import Vehicle
import datetime

def from_db_to_car(res):
    #garante que o campo created_at (res[4]) seja datetime, não string
    created_at = res[4]
    if isinstance(created_at, str):
        try:
            #tenta converter se vier em string do banco
            created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            #caso venha com milissegundos
            created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

    carro = Vehicle(
        id=res[0],
        placa=res[1],
        parked=res[3],
        modelo=res[2],
        horario_entrada=created_at,
        locale=res[5],
    )

    return carro.toDictionary()
