from db.database import connection
from repositories.car_logs_repository import total_cars_logs, find_by_plate_on_history, list_cars_history
import datetime


def consult_cars_logs(license_plate: str = None, page: int = 1, limit: int = 10):
        try:
            columns = ['id', 'car_id', 'license_plate', 'model', 'locale', 'parked', 'created_at', 'removed_at', 'price']
            with connection.cursor() as cursor:
                total = total_cars_logs(cursor)
                if license_plate:
                    carro_dict = find_by_plate_on_history(cursor, license_plate)
                    if not carro_dict:
                        return {"message": "Carro não encontrado"}, 404

                    print(
                        f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Consulta unitária realizada com sucesso!")
                    return {
                        "carros": [
                            carro_dict
                        ],
                        "totalSearch": 1,
                        "totalVehicles": total,

                    }, 200

                offset = (page - 1) * limit
                results = list_cars_history(cursor, limit, offset)


                cars = [dict(zip(columns, car)) for car in results]

                for car in cars:
                    if isinstance(car['created_at'], datetime.datetime):
                        car['created_at'] = car['created_at'].strftime('%Y-%m-%dT%H:%M:%S')
                    if isinstance(car['removed_at'], datetime.datetime):
                        car['removed_at'] = car['removed_at'].strftime('%Y-%m-%dT%H:%M:%S')

                if not cars:
                    return {"message": "Não há carros no sistema"}, 404

                print(
                    f"[INFO]:[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Consulta realizada com sucesso!")

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