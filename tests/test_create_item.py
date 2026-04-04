import allure
import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"


# TC-POST-001: Успешное создание объявления
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-001: Успешное создание объявления")
@allure.description("Проверка создания объявления с валидными данными")
def test_create_item_success(create_item):
    with allure.step("Создание объявления"):
        response, payload = create_item()

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 200, (
            f"Создание валидного объявления"
            f" закончилось со статусом {response.status_code}, ожидался статус 200"
        )
    data = response.json()

    with allure.step("Проверка структуры и данных"):
        assert "id" in data, "В ответе нет поля id"
        assert data["name"] == payload["name"], "В ответе поля name не совпадают"
        assert data["price"] == payload["price"], "В ответе поля price  не совпадают"
        assert (
            data["sellerId"] == payload["sellerId"]
        ), "В ответе поля sellerId  не совпадают"
        assert (
            data["statistics"] == payload["statistics"]
        ), "В ответе поля statistics  не совпадают"


# TC-POST-002: Проверка уникальности id и неуникальности других полей
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-002: Проверка уникальности id и неуникальности других полей")
def test_create_item_unique_id(create_item):
    with allure.step("Создание двух объявлений"):
        resp1, _ = create_item()
        resp2, _ = create_item()

    with allure.step("Проверка статус-кодов"):
        assert resp1.status_code == 200, (
            f"Создание первого объявления "
            f"закончилось со статусом {resp1.status_code}, ожидался статус 200"
        )
        assert resp2.status_code == 200, (
            f"Создание второго такого же "
            f"объявления закончилось со статусом {resp2.status_code}, ожидался статус 200"
        )

    id1 = resp1.json()["status"].split(" - ")[1]
    id2 = resp2.json()["status"].split(" - ")[1]

    with allure.step("Проверка уникальности id"):
        assert id1 != id2, "У двух объявлений совпали id"


# TC-POST-003: Создание объявления с нулевыми полями статистики
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-003: Создание объявления с нулевыми полями статистики")
@pytest.mark.parametrize(
    "likes, view_count, contacts, null_field",
    [(0, 1, 1, "likes"), (1, 0, 1, "view_count"), (1, 1, 0, "contacts")],
)
def test_create_item_zero_statistics(
    create_item, likes, view_count, contacts, null_field
):
    with allure.step(f"Создание объявления с нулевым полем {null_field}"):
        response, _ = create_item(likes=likes, view_count=view_count, contacts=contacts)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 200, (
            f"Создание объявления с нулевым полем "
            f"{null_field} закончилось со статусом {response.status_code}, ожидался статус 200"
        )


# TC-POST-004: Создание объявления с нулевой ценой
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-004: Создание объявления с нулевой ценой")
def test_create_item_zero_price(create_item):
    with allure.step("Создание объявления с price=0"):
        response, _ = create_item(price=0)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 200, (
            f"Создание объявления с нулевой "
            f"ценой закончилось со статусом {response.status_code}, ожидался статус 200"
        )


# TC-POST-005: Создание объявления с пустым полем name
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-005: Создание объявления с пустым полем name")
def test_create_item_empty_name(create_item):
    with allure.step("Создание объявления с пустым name"):
        response, _ = create_item(name="")

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Создание объявления с пустым "
            f"полем name закончилось со статусом {response.status_code}, ожидался статус 400"
        )


# TC-POST-006: Создание объявления без одного поля
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-006: Создание объявления без одного поля")
@pytest.mark.parametrize("field", [("name"), ("price"), ("statistics"), ("sellerID")])
def test_create_item_no_one_field(field):
    payload = {
        "sellerID": 435627,
        "name": "test item",
        "price": 200,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }
    with allure.step(f"Удаление поля {field}"):
        del payload[field]
    with allure.step("Отправка POST запроса"):
        response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        allure.attach(str(payload), "Payload", allure.attachment_type.JSON)
        allure.attach(response.text, "Response", allure.attachment_type.JSON)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Создание объявления без"
            f"{field} закончилось со статусом {response.status_code}, ожидался статус 400"
        )


# TC-POST-007: Создание объявления c отрицательной ценой
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-007: Создание объявления c отрицательной ценой")
def test_create_item_negative_price(create_item):
    with allure.step("Создание объявления с отрицательной ценой"):
        response, _ = create_item(price=-100)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Создание объявления с "
            f"отрицательной ценой закончилось со статусом {response.status_code}, ожидался статус 400"
        )


# TC-POST-008: Создание объявления c нецелой ценой
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-008: Создание объявления c нецелой ценой")
def test_create_item_float_price(create_item):
    with allure.step("Создание объявления с float ценой"):
        response, _ = create_item(price=10.5)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Создание объявления с нецелой "
            f"ценой закончилось со статусом {response.status_code}, ожидался статус 400"
        )


# TC-POST-009: Создание объявления c отрицательной статистикой
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-009: Создание объявления c отрицательной статистикой")
@pytest.mark.parametrize(
    "likes, view_count, contacts, neg_field",
    [(-1, 1, 1, "likes"), (1, -1, 1, "view_count"), (1, 1, -1, "contacts")],
)
def test_create_item_negative_statistics(
    create_item, likes, view_count, contacts, neg_field
):
    with allure.step(f"Создание объявления с отрицательным {neg_field}"):
        response, _ = create_item(likes=likes, view_count=view_count, contacts=contacts)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Создание объявления с "
            f"отрицательным полем {neg_field} закончилось со статусом "
            f"{response.status_code}, ожидался статус 400"
        )


# TC-POST-010: Создание объявления c нецелой статистикой
@allure.feature("Item")
@allure.story("Создание объявления")
@allure.title("TC-POST-010: Создание объявления c нецелой статистикой")
@pytest.mark.parametrize(
    "likes, view_count, contacts, float_field",
    [(1.2, 1, 1, "likes"), (1, 1.5, 1, "view_count"), (1, 1, 1.8, "contacts")],
)
def test_create_item_float_statistics(
    create_item, likes, view_count, contacts, float_field
):
    with allure.step(f"Создание объявления с float {float_field}"):
        response, _ = create_item(likes=likes, view_count=view_count, contacts=contacts)

    with allure.step("Проверка статус-кода"):
        assert response.status_code == 400, (
            f"Создание объявления с "
            f"нецелым полем {float_field} закончилось со статусом "
            f"{response.status_code}, ожидался статус 400"
        )
