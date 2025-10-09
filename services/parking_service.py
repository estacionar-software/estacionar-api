import datetime # Biblioteca para horários
import math # Biblioteca para Operações Matematicas
from models.car import Carro # Importando da pasta models do arquivo car, a classe Carro
from database import connection # Importando o conector do banco de dados

time_now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

def cadastrarCarro(id: str, license_plate: str, model: str): # Função para cadastrar carro novo no banco de dados
    license_plate = license_plate.upper()
    try:
        with connection.cursor() as cursor: # Garante abertura e fechamento seguro do cursor
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s''' # Consulta sql, seleciona todos na table cars_parked onde license_plate seja igual ao license_plate digitado pelo user
            cursor.execute(search_vehicle, (license_plate,)) # Executa a consulta sql passando a consulta de search_vehicle e a license plate que quero verificar
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
            print(f"[INFO]:[{time_now}] {novo_carro.modelo} de placa {license_plate} (ID: {novo_carro.id}) adicionado ao sistema.")
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

                carro_dict = Carro(
                    id = res[0],
                    placa=res[1],
                    parked = res[3],
                    modelo=res[2],
                    horario_entrada=res[4],
                ).toDictionary()

                print(carro_dict)

                print(f"[INFO]:[{time_now}] Consulta unitária realizada com sucesso!")
                return carro_dict, 200

            all_vehicles = '''SELECT * FROM cars_parked'''
            cursor.execute(all_vehicles)
            results = cursor.fetchall()
            cars = [dict(zip(columns, car)) for car in results]
            if not cars:
                return {"mensagem": "Não há carros no sistema"}, 404
            print(f"[INFO]:[{time_now}] Consulta realizada com sucesso!")

            return cars, 200
    except Exception as ex:
        connection.rollback()
        return {"mensagem": str(ex), "carro": None}, 400

def calculate_price(enter_time):
    exit_hour = datetime.datetime.now()
    enter_time = datetime.datetime.strptime(enter_time, '%Y-%m-%dT%H:%M:%S')
    length_of_stay = exit_hour - enter_time

    total_seconds = int(length_of_stay.total_seconds())
    hours, resto = divmod(total_seconds, 3600)
    minutes, _ = divmod(resto, 60)

    if total_seconds <= 1800:
        value = 7
        time = f"{minutes} minutos"
        return time, value, exit_hour
    elif total_seconds <= 10800:
        value = 13
        time = f"{hours}h{minutes:02d}m"
        return time, value, exit_hour

    overtime_in_seconds = total_seconds - 10800
    overtime = math.ceil(overtime_in_seconds / 3600)
    total_price = 13 + (overtime * 2)
    total_time = f"{hours}h{minutes:02d}m"

    return total_time, total_price, exit_hour

def removerCarro(license_plate: str):
    try:
        with connection.cursor() as cursor:
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
            cursor.execute(search_vehicle, (license_plate.upper(),))
            res = cursor.fetchone()
            if not res:
                return {"mensagem": "Carro não encontrado"}, 404

            delete_car = '''DELETE FROM cars_parked WHERE id = %s;'''
            car = Carro(
                id=res[0],
                placa=res[1],
                parked=res[3],
                modelo=res[2],
                horario_entrada=res[4],
            ).toDictionary()

            print(car)

            total_time, total_price, exit_hour = calculate_price(car['created_at'])
            car.update({
                "total_price": total_price,
                "total_time": total_time,
                "exit_hour": exit_hour
            })
            cursor.execute(delete_car, (car['id'],))
            connection.commit()
        print(f"[INFO]:[{time_now}] {car['model']} de placa {license_plate} (ID: {car['id']}) removido do sistema")
        return {"message": "Veiculo excluído com sucesso.", "data": car }, 200

    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "carro": None}, 400

def update_car(plate, new_license_plate: str, model: str):

    try:
        with connection.cursor() as cursor:
            search_vehicle = '''SELECT * FROM cars_parked WHERE license_plate = %s'''
            cursor.execute(search_vehicle, (plate.upper(),))
            res = cursor.fetchone()

            if not res:
                return {"mensagem": "Carro não encontrado"}, 404

            car = Carro(
                id=res[0],
                placa=res[1],
                parked=res[3],
                modelo=res[2],
                horario_entrada=res[4],
            ).toDictionary()

            if new_license_plate and model:
                update = """UPDATE cars_parked SET model = %s, license_plate = %s WHERE license_plate = %s"""
                cursor.execute(update, (model, new_license_plate, plate))
                connection.commit()

                car.update({
                    "license_plate": new_license_plate,
                    "model": model
                })

                print(f"[INFO]:[{time_now}] ATUALIZAÇÃO DE MODELO E PLACA NO SISTEMA: (ID: {car['id']})")
                return {"message": "Veiculo atualizado com sucesso.", "carro": car}, 200

            if new_license_plate:

                update = """UPDATE cars_parked SET license_plate = %s WHERE license_plate = %s"""
                cursor.execute(update, (new_license_plate, plate))
                connection.commit()

                car.update({
                    "license_plate": new_license_plate,
                })

            if model:
                update = """UPDATE cars_parked SET model = %s WHERE license_plate = %s"""
                cursor.execute(update, (model, plate))
                connection.commit()

                car.update({
                    "model": model
                })

            print(f"[INFO]:[{time_now}] ATUALIZAÇÃO NO SISTEMA: (ID: {car['id']})")
            return {"message": "Veiculo atualizado com sucesso.", "carro": car}, 200
    except Exception as ex:
        connection.rollback()
        return {"message": str(ex), "carro": None}, 400
