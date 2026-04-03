import requests
import pytest

BASE_URL = "https://qa-internship.avito.com"

#TC-STAT-001: Получение статистики
def test_get_statistics_success(create_item):
    response, payload = create_item(likes=5, view_count=10, contacts=2)
    item_id = response.json()["status"].split(' - ')[1]

    resp = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")

    assert resp.status_code == 200 , (f"Получение статистики завершилось "
    f"со статусом {get_resp.status_code}, ожидался статус 200 - ОК")

    stats = resp.json()[0]
    assert stats["likes"] == 5 , f"Неверное likes"
    assert stats["viewCount"] == 10 , f"Неверное viewCount"
    assert stats["contacts"] == 2 , f"Неверное contacts"


#TC-STAT-002: Проверка идемпотичности
def test_get_statistics_idempotency(create_item):
    response, _ = create_item()
    item_id = response.json()["status"].split(' - ')[1]

    r1 = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")
    r2 = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")

    assert r1.status_code == 200 , (f"Получение первой статистики завершилось "
    f"со статусом {r1.status_code}, ожидался статус 200 - ОК")
    assert r2.status_code == 200 , (f"Получение второй такой же статистики завершилось "
    f"со статусом {r2.status_code}, ожидался статус 200 - ОК")
    assert r1.json() == r2.json() , f"Ответ, полученный при первом и втором запросах, различается"


#TC-STAT-003: Получение статистики по id неверной длины
@pytest.mark.parametrize("invalid_id", [
    ("aea31596-0d05-4097-bb19-afdd4503141f23"),
    ("aea31596-0d05-4097-bb19-afdd45031")
])
def test_get_statistics_invalid_id(invalid_id):
    response = requests.get(f"{BASE_URL}/api/1/statistic/{invalid_id}")

    assert response.status_code == 400 , (f"Получение статистики по id неверной длины "
    f"завершилось со статусом {response.status_code}, ожидался статус 400")


#TC-STAT-004: Получение статистики по несуществующему id
@pytest.mark.parametrize("nonexist_id", [
    ("aea31596-0d05-4097-bb19-afdd4503143f"),
    ("aea31596-0d05-4097-bb19-afdd4504243f")
])
def test_get_statistics_not_found(nonexist_id):
    response = requests.get(f"{BASE_URL}/api/1/statistic/{nonexist_id}")

    assert response.status_code == 404 , (f"Получение статистики по несуществующему id "
    f"завершилось со статусом {response.status_code}, ожидался статус 404")
