from flask import Flask, request, jsonify
from services.parking_service import cadastrarCarro, consultarCarros, removerCarro

app = Flask(__name__)

@app.route("/carros", methods=["POST"])
def cadastrar():
    dados = request.json
    resposta, status = cadastrarCarro(dados["placa"], dados["cor"], dados["modelo"])
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

app.run()
