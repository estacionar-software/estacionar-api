from flask import Flask, request, jsonify
import uuid
from services.parking_service import cadastrarCarro, consultarCarros, removerCarro, update_car

app = Flask(__name__) 


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

if __name__ == "__main__":
    app.run(debug=True)
