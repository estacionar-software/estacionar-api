from flask import Flask, request, jsonify
import uuid
from services.parking_service import cadastrarCarro, consultarCarros, removerCarro, update_car
from services.parking_fees_service import create_price, get_price, update_price, delete_price
from flask_cors import CORS
app = Flask(__name__) 

CORS(app)

# ABAIXO, INICIA AS ROTAS PARA OS CARROS ESTACIONADOS.

@app.route("/carros", methods=["POST"])
def cadastrar():
    id = str(uuid.uuid4())
    dados = request.json
    resposta, status = cadastrarCarro(id, dados["license_plate"], dados["model"], dados["locale"])
    return jsonify(resposta), status

@app.route("/carros", methods=["GET"])
def listar():
    placa = request.args.get("placa")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)

    resposta, status = consultarCarros(placa, page, limit)
    return jsonify(resposta), status

@app.route("/carros/<placa>", methods=["DELETE"])
def remover(placa):
    resposta, status = removerCarro(placa)
    return jsonify(resposta), status

@app.route("/carros/<placa>", methods=["PUT"])
def atualizar(placa):
    dados = request.json
    resposta, status = update_car(placa, dados["license_plate"], dados["model"], dados["locale"])

    return jsonify(resposta), status

# ABAIXO, INICIA AS ROTAS OS PREÇOS DE ESTACIONAMENTO.

@app.route("/price", methods=["POST"])
def create_price_for_parking():
    data = request.json
    response, status = create_price(data["tolerance_time"], data["quick_stop_price"], data["until_time_price"], data["extra_hour_price"])
    
    return jsonify(response), status

@app.route("/price", methods=["GET"])
def get_price_for_parking():
    response, status = get_price()

    return jsonify(response), status

@app.route("/price", methods=["PUT"])
def update_price_for_parking():
    data = request.json
    response, status = update_price(data["tolerance_time"], data["quick_stop_price"], data["until_time_price"], data["extra_hour_price"])

    return jsonify(response), status

@app.route("/price", methods=["DELETE"])
def delete_price_for_parking():
    response, status = delete_price()

    return jsonify(response), status


if __name__ == "__main__":
    app.run(debug=True, port=5001)
