import pytest
import requests

BASE_URL = "http://127.0.0.1:5001"
vehicle_plate = "UYA1234"
model = "Toyota Yaris"
locale = "Setor 5"

def test_create_new_parked_car():
    new_vehicle_parked = {
        "license_plate": vehicle_plate,
        "model": model,
        "locale": locale,
    }
    res = requests.post(f"{BASE_URL}/vehicles", json=new_vehicle_parked)
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["message"] == "Veiculo cadastrado com sucesso!"
    assert "vehicle" in res_json
    assert res_json["vehicle"]["license_plate"] == vehicle_plate

def test_get_cars_parked():
    res = requests.get(f"{BASE_URL}/vehicles?page=1&limit=10")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["limit"] == 10
    assert res_json["page"] == 1
    assert len(res_json["vehicles"]) == 10

def test_get_one_car_parked():
    res = requests.get(f"{BASE_URL}/vehicles?placa={vehicle_plate}")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["vehicles"][0]['license_plate'] == vehicle_plate
    assert res_json["vehicles"][0]['model'] == model
    assert res_json["vehicles"][0]['locale'] == locale

def test_delete_car_parked():
    res = requests.delete(f"{BASE_URL}/vehicles/{vehicle_plate}")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["message"] == "Veiculo excluído com sucesso."
    assert res_json["data"]["license_plate"] == vehicle_plate

