import pytest
import requests

BASE_URL = "http://127.0.0.1:5001"
car_plate = "JHS2131"
model = "Toyota Yaris"
locale = "Setor 5"

def test_create_new_parked_car():
    new_car_parked = {
        "license_plate": car_plate,
        "model": model,
        "locale": locale,
    }
    res = requests.post(f"{BASE_URL}/carros", json=new_car_parked)
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["mensagem"] == "Carro cadastrado com sucesso!"
    assert "carro" in res_json
    assert res_json["carro"]["license_plate"] == car_plate

def test_get_cars_parked():
    res = requests.get(f"{BASE_URL}/carros?page=1&limit=10")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["limite"] == 10
    assert res_json["pagina"] == 1
    assert len(res_json["carros"]) == 10

def test_get_one_car_parked():
    res = requests.get(f"{BASE_URL}/carros?placa={car_plate}")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["carros"][0]['license_plate'] == car_plate
    assert res_json["carros"][0]['model'] == model
    assert res_json["carros"][0]['locale'] == locale

def test_delete_car_parked():
    res = requests.delete(f"{BASE_URL}/carros/{car_plate}")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["message"] == "Veiculo excluído com sucesso."
    assert res_json["data"]["license_plate"] == car_plate

