import datetime

#Classe de um carro
class Carro:
    def __init__(self, placa: str, cor: str, modelo: str): #Atributos da classe Carro
        self.placa = placa.upper()
        self.cor = cor
        self.modelo = modelo
        self.horarioEntrada = datetime.datetime.now()

    def toDictionary(self): #Esse metodo pode ser usada para transformar o objeto em algo que o flask consegue serializar pro JSON
        return {
            "placa": self.placa,
            "cor": self.cor,
            "modelo": self.modelo,
            "horarioEntrada": self.horarioEntrada.isoformat()
        }