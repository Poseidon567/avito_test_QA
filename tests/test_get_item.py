import requests
import pytest

BASE_URL = "https://qa-internship.avito.com"

#TC-GET-001: Получение существующего объявления
def test_get_item_success(create_item):
    response, payload = create_item()
    item_id = response.json()["status"].split(' - ')[1]
    get_resp = requests.get(f"{BASE_URL}/api/1/item/{item_id}")

    assert get_resp.status_code == 200, (f"Получение объявления завершилось "
    f"со статусом {get_resp.status_code}, ожидался статус 200 - ОК")

    data = get_resp.json()[0]
    assert data["id"] == item_id , f"Неверное id"
    assert data["name"] == payload["name"] , f"Неверное name"
    assert data["price"] == payload["price"] , f"Неверное price"
    assert data["statistics"] == payload["statistics"] , f"Неверное statistics"
    assert data["sellerId"] == payload["sellerId"] , f"Неверное sellerId"
    

#TC-GET-002: Проверка идемпотентности
def test_get_item_idempotency(create_item):
    response, _ = create_item()
    item_id = response.json()["status"].split(' - ')[1]

    r1 = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    r2 = requests.get(f"{BASE_URL}/api/1/item/{item_id}")

    assert r1.status_code == 200 , (f"Получение первого объявления завершилось "
    f"со статусом {r1.status_code}, ожидался статус 200 - ОК")
    assert r2.status_code == 200 , (f"Получение второго такого же объявления завершилось "
    f"со статусом {r2.status_code}, ожидался статус 200 - ОК")
    assert r1.json() == r2.json(), f"Ответ, полученный при первом и втором запросах, различается"

#TC-GET-003: Получение объявления по id неверной длины
@pytest.mark.parametrize("invalid_id", [
    ("aea31596-0d05-4097-bb19-afdd4503141f23"),
    ("aea31596-0d05-4097-bb19-afdd45031")
])
def test_get_item_invalid_id(invalid_id):
    response = requests.get(f"{BASE_URL}/api/1/item/{invalid_id}")

    assert response.status_code == 400, (f"Получение объявления по id неверной длины "
    f"завершилось со статусом {response.status_code}, ожидался статус 400")

#TC-GET-004: Получение объявления по несуществующему id
@pytest.mark.parametrize("nonexist_id", [
    ("aea31596-0d05-4097-bb19-afdd4503143f"),
    ("aea31596-0d05-4097-bb19-afdd4504243f")
])
def test_get_item_not_found(nonexist_id):
    response = requests.get(f"{BASE_URL}/api/1/item/{nonexist_id}")

    assert response.status_code == 404, (f"Получение объявления по несуществующему id "
    f"завершилось со статусом {response.status_code}, ожидался статус 404")
