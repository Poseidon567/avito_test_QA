import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"


# TC-SELLER-001: Получение списка объявлений продавца
def test_get_seller_items(create_item):
    response, payload = create_item()
    seller_id = payload["sellerId"]

    resp = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")

    assert resp.status_code == 200, (
        f"Получение объявлений по sellerID закончилось"
        f" со статусом {resp.status_code}, ожидался статус 200"
    )

    for item in resp.json():
        assert item["sellerId"] == seller_id, "У объявления другой sellerID"


# TC-SELLER-002: Получение списка объявлений с нечисловым sellerID
@pytest.mark.parametrize("invalid_id", [("523647fg"), ("523647.3")])
def test_get_seller_items_invalid_id(invalid_id):
    response = requests.get(f"{BASE_URL}/api/1/{invalid_id}/item")

    assert response.status_code == 400, (
        f"Получение объявлений по нечисловому sellerID закончилось"
        f" со статусом {response.status_code}, ожидался статус 400"
    )


# TC-SELLER-003: Получение списка объявлений с пустым sellerID
def test_get_seller_items_empty_id():
    response = requests.get(f"{BASE_URL}/api/1//item")

    assert response.status_code == 400, (
        f"Получение объявлений по пустому sellerID закончилось"
        f" со статусом {response.status_code}, ожидался статус 400"
    )
