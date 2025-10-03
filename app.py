from flask import Flask, request, jsonify
import uuid
from services.parking_service import cadastrarCarro, consultarCarros, removerCarro

app = Flask(__name__) 

@app.route("/carros", methods=["POST"])
def cadastrar():
    id = str(uuid.uuid4())
    dados = request.json
    resposta, status = cadastrarCarro(id, dados["license_plate"], dados["model"])
    return jsonify(resposta), status

@app.route("/carros", methods=["GET"])
def listar():
    placa = request.args.get("placa")
    resposta, status = consultarCarros(placa)
    return jsonify(resposta), status

@app.route("/carros/<placa>", methods=["DELETE"])
def remover(placa):
    resposta, status = removerCarro(placa)
    return jsonify(resposta), status

if __name__ == "__main__":
    app.run(debug=True)
