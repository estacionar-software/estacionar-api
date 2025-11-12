import pytest
import requests

BASE_URL = "http://127.0.0.1:5001"
extra_hour_price = 1
parking_hours = 3
quick_stop_limit_minutes = 30
quick_stop_price = 5
until_time_price = 12

def test_create_new_parking_fees():
    new_parking_fees = {
        "extra_hour_price": extra_hour_price,
        "parking_hours": parking_hours,
        "quick_stop_limit_minutes": quick_stop_limit_minutes,
        "quick_stop_price": quick_stop_price,
        "until_time_price": until_time_price
    }
    res = requests.post(f"{BASE_URL}/price-parking", json=new_parking_fees)
    assert res.status_code == 201
    res_json = res.json()
    assert "message" in res_json
    assert res_json["message"] == "Preços adicionado ao sistema!"

def test_get_parking_fees():
    res = requests.get(f"{BASE_URL}/price-parking")
    assert res.status_code == 200
    res_json = res.json()
    assert "message" in res_json
    assert "prices" in res_json
    assert res_json["prices"]['parking_hours'] == parking_hours

def test_update_parking_fees():
    extra_hour_price = 5
    new_parking_fees = {
        "extra_hour_price": extra_hour_price,
    }
    res = requests.put(f"{BASE_URL}/price-parking", json=new_parking_fees)
    assert res.status_code == 200
    res_json = res.json()
    assert "message" in res_json
    assert "prices" in res_json
    assert res_json["message"] == "Preços atualizados com sucesso"
    assert res_json["prices"]['extra_hour_price'] == extra_hour_price

def test_remove_parking_fees():
    res = requests.delete(f"{BASE_URL}/price-parking")
    assert res.status_code == 200
    res_json = res.json()
    assert "message" in res_json

