import datetime
import math

carrosEstacionados = []

def cadastrarCarro():
    placa = input("Digite a placa: ").upper()
    cor = input("Digite a cor do veiculo: ")
    modelo = input("Digite o modelo do veiculo: ")

    for carro in carrosEstacionados:
        if carro['placa'] == placa:
            print("Carro Ja Cadastrado!")
            break

    hora = datetime.datetime.now()

    carrosEstacionados.append({
        "placa": placa,
        "cor": cor,
        "modelo": modelo,
        "horarioEntrada": hora,
    })
    print("Carro Cadastrado!")


def consultarCarros():

    decisao = input("O Que deseja consultar? \n 1 - Carro pela placa \n 2 - Todos os veiculos estacionados \n")

    if decisao == "1":

        placa = input("Digite a placa: ").upper()

        for carro in carrosEstacionados:
            if carro['placa'] == placa:
                print(f"Placa: {carro['placa']} | Modelo: {carro['modelo']} | Cor: {carro['cor']} | Entrada: {carro['horarioEntrada'].strftime('%H:%M')}")
    elif decisao == "2":
        for carro in carrosEstacionados:
            print(f"Placa: {carro['placa']} | Modelo: {carro['modelo']} | Cor: {carro['cor']} | Entrada: {carro['horarioEntrada'].strftime('%H:%M')}")


def calcularValor(horarioEntrada):

    horaSaida = datetime.datetime.now()

    tempoPermanencia = horaSaida - horarioEntrada

    totalSegundos = int(tempoPermanencia.total_seconds())
    horas, resto = divmod(totalSegundos, 3600)
    minutos, segundos = divmod(resto, 60)
    if totalSegundos <= 1800:
        print(f"Valor total a ser pago é: \nR$7,00\nTempo de permanência: {minutos:02d} Minutos" )
    elif totalSegundos <= 10800:
        print(f"Valor total a ser pago é: \nR$13,00\nTempo de permanência:\n{horas:2d}:{minutos:02d}\n{horas:2d} hora e {minutos:02d} minutos" )

    horasExtrasSegundos = totalSegundos - 10800

    if horasExtrasSegundos > 0:
        horasExtras = math.ceil(horasExtrasSegundos / 3600)
        valorFinal = 13 + (horasExtras * 2)

        print(f"Valor total a ser pago é: \nR${valorFinal}\nTempo de permanência:\n{horas:2d}:{minutos:02d}\n{horas:2d} hora e {minutos:02d} minutos")

def removerCarros():
    placa = input("Digite a placa: ").upper()

    for carro in carrosEstacionados:
        if carro['placa'] == placa:
            print(f"Placa: {carro['placa']} | Modelo: {carro['modelo']} | Cor: {carro['cor']} | Entrada: {carro['horarioEntrada'].strftime('%H:%M')}")
            calcularValor(carro['horarioEntrada'])

while True:
    print("\n=== Sistema de Estacionamento ===")
    print("1 - Cadastrar carro")
    print("2 - Consultar carros")
    print("3 - Remover carro / Calcular valor")
    print("4 - Sair")

    opcao = input("Digite o número da opção desejada: ")

    if opcao == "1":
        cadastrarCarro()
    elif opcao == "2":
        consultarCarros()
    elif opcao == "3":
        removerCarros()
    elif opcao == "4":
        print("Saindo do sistema. Até logo!")
        break
    else:
        print("Opção inválida! Tente novamente.")