from flask import Flask, request, jsonify
import uuid

from services.cars_logs_service import consult_cars_logs
from services.parking_service import post_vehicle, read_vehicles, remove_vehicle, update_vehicle
from services.parking_fees_service import create_price, get_price, update_price, delete_price
from services.products_and_services_service import create_product_or_service, get_product_or_service, update_product_or_service, delete_product_or_service
from flask_cors import CORS
app = Flask(__name__) 

CORS(app)

# ABAIXO, INICIA AS ROTAS PARA OS CARROS ESTACIONADOS.

@app.route("/vehicles", methods=["POST"])
def cadastrar():
    id = str(uuid.uuid4())
    dados = request.json
    response, status = post_vehicle(id, dados["license_plate"], dados["model"], dados["locale"])
    return jsonify(response), status

@app.route("/vehicles", methods=["GET"])
def listar():
    plate = request.args.get("plate")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    order = request.args.get("order", default="DESC", type=str)

    response, status = read_vehicles(order, plate, page, limit)
    return jsonify(response), status

@app.route("/vehicles/<plate>", methods=["DELETE"])
def remover(plate):
    response, status = remove_vehicle(plate)
    return jsonify(response), status

@app.route("/vehicles/<plate>", methods=["PUT"])
def atualizar(plate):
    data = request.json
    response, status = update_vehicle(plate, data["license_plate"], data["model"], data["locale"])

    return jsonify(response), status

# ROTA PARA CONSEGUIR OS LOGS DE CARROS ANTERIORES
@app.route("/vehicles-logs", methods=["GET"])
def get_cars_logs():
    plate = request.args.get("plate")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    order = request.args.get("order", default="DESC", type=str)

    response, status = consult_cars_logs(order, plate, page, limit)
    return jsonify(response), status

# ABAIXO, INICIA AS ROTAS OS PREÇOS DE ESTACIONAMENTO.

@app.route("/price-parking", methods=["POST"])
def create_price_for_parking():
    data = request.json
    response, status = create_price(data["parking_hours"], data["quick_stop_price"], data["until_time_price"], data["extra_hour_price"], data["quick_stop_limit_minutes"])
    return jsonify(response), status

@app.route("/price-parking", methods=["GET"])
def get_price_for_parking():
    response, status = get_price()
    return jsonify(response), status

@app.route("/price-parking", methods=["PUT"])
def update_price_for_parking():
    data = request.json

    response, status = update_price(
        parking_hours=data.get("parking_hours"),
        quick_stop_price=data.get("quick_stop_price"),
        until_time_price=data.get("until_time_price"),
        quick_stop_limit_minutes=data.get("quick_stop_limit_minutes"),
        extra_hour_price=data.get("extra_hour_price")
    )
    return jsonify(response), status

@app.route("/price-parking", methods=["DELETE"])
def delete_price_for_parking():
    response, status = delete_price()
    return jsonify(response), status

# PRODUTOS E SERVIÇOS

@app.route("/products", methods=["POST"])
def create_products_and_services():
    id = str(uuid.uuid4())
    data = request.json
    response, status = create_product_or_service(id, data["description"], data["title"], data["amount"], data["price"], data["type"])
    return jsonify(response), status

@app.route("/products", methods=["GET"])
def get_products_and_services():
    response, status = get_product_or_service()
    return jsonify(response), status

@app.route("/products/<id>", methods=["PUT"])
def update_products_and_services(id):
    data = request.json
    response, status = update_product_or_service(
        id,
        title=data.get("title"),
        description=data.get("description"),
        amount=data.get("amount"),
        price=data.get("price"),
        type=data.get("type")
    )
    return jsonify(response), status

@app.route("/products/<id>", methods=["DELETE"])
def delete_products_and_services(id):
    response, status = delete_product_or_service(id)
    return jsonify(response), status

if __name__ == "__main__":
    app.run(debug=True, port=5001)
