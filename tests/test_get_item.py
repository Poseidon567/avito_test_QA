import allure
import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"


# TC-GET-001: Получение существующего объявления
@allure.feature("Item")
@allure.story("Получение объявления по id")
@allure.title("TC-GET-001: Получение существующего объявления")
def test_get_item_success(create_item):
    with allure.step("Создание объявления"):
        response, payload = create_item()
    item_id = response.json()["status"].split(" - ")[1]

    with allure.step("GET запрос"):
        get_resp = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
        allure.attach(get_resp.text, "Response", allure.attachment_type.JSON)

    with allure.step("Проверка статус-кода"):
        assert get_resp.status_code == 200, (
            f"Получение объявления завершилось "
            f"со статусом {get_resp.status_code}, ожидался статус 200 - ОК"
        )

    data = get_resp.json()[0]

    with allure.step("Проверка данных"):
        assert data["id"] == item_id, "Неверное id"
        assert data["name"] == payload["name"], "Неверное name"
        assert data["price"] == payload["price"], "Неверное price"
        assert data["statistics"] == payload["statistics"], "Неверное statistics"
        assert data["sellerId"] == payload["sellerId"], "Неверное sellerId"


# TC-GET-002: Проверка идемпотентности
@allure.feature("Item")
@allure.story("Получение объявления по id")
@allure.title("TC-GET-002: Проверка идемпотентности")
def test_get_item_idempotency(create_item):

    with allure.step("Создание объявления"):
        response, _ = create_item()
    item_id = response.json()["status"].split(" - ")[1]

    with allure.step("Два GET запроса"):
        r1 = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
        r2 = requests.get(f"{BASE_URL}/api/1/item/{item_id}")

    with allure.step("Проверки статус-кодов"):
        assert r1.status_code == 200, (
            f"Получение первого объявления завершилось "
            f"со статусом {r1.status_code}, ожидался статус 200 - ОК"
        )
        assert r2.status_code == 200, (
            f"Получение второго такого же объявления завершилось "
            f"со статусом {r2.status_code}, ожидался статус 200 - ОК"
        )
    with allure.step("Сравнение ответов"):
        assert (
            r1.json() == r2.json()
        ), "Ответ, полученный при первом и втором запросах, различается"


# TC-GET-003: Получение объявления по id неверной длины
@allure.feature("Item")
@allure.story("Получение объявления по id")
@allure.title("TC-GET-003: Получение объявления по id неверной длины")
@pytest.mark.parametrize(
    "invalid_id",
    [("aea31596-0d05-4097-bb19-afdd4503141f23"), ("aea31596-0d05-4097-bb19-afdd45031")],
)
def test_get_item_invalid_id(invalid_id):

    with allure.step(f"GET запрос с id {invalid_id}"):
        response = requests.get(f"{BASE_URL}/api/1/item/{invalid_id}")

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Получение объявления по id неверной длины "
            f"завершилось со статусом {response.status_code}, ожидался статус 400"
        )


# TC-GET-004: Получение объявления по несуществующему id
@allure.feature("Item")
@allure.story("Получение объявления по id")
@allure.title("TC-GET-004: Получение объявления по несуществующему id")
@pytest.mark.parametrize(
    "nonexist_id",
    [
        ("aea31596-0d05-4097-bb19-afdd4503143f"),
        ("aea31596-0d05-4097-bb19-afdd4504243f"),
    ],
)
def test_get_item_not_found(nonexist_id):

    with allure.step(f"GET запрос с id {nonexist_id}"):
        response = requests.get(f"{BASE_URL}/api/1/item/{nonexist_id}")

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 404, (
            f"Получение объявления по несуществующему id "
            f"завершилось со статусом {response.status_code}, ожидался статус 404"
        )
