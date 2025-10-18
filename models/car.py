import datetime

#Classe de um carro
class Carro:
    def __init__(self, id: str, placa: str, parked: bool, modelo: str, locale: str, horario_entrada: datetime.datetime = None): #Atributos da classe Carro
        self.id = id
        self.placa = placa.upper()
        self.parked = parked
        self.modelo = modelo
        self.horarioEntrada = horario_entrada or datetime.datetime.now()
        self.locale = locale

    def toDictionary(self): #Esse metodo pode ser usado para transformar o objeto em algo que o flask consegue serializar pro JSON
        return {
            "id": self.id,
            "license_plate": self.placa,
            "parked": self.parked,
            "model": self.modelo,
            "created_at": self.horarioEntrada.isoformat(),
            "locale": self.locale,
        }