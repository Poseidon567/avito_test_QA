import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"


@pytest.fixture(scope="function")
def create_item():
    created_items = []
    def _create_item(
        seller_id=523647,
        name="test item",
        price=100,
        likes=1,
        view_count=1,
        contacts=1,
    ):

        payload = {
            "sellerId": seller_id,
            "name": name,
            "price": price,
            "statistics": {
                "likes": likes,
                "viewCount": view_count,
                "contacts": contacts,
            },
        }

        response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        if response.status_code == 200:
            created_items.append(response.json()["status"])
        return response, payload

        

    yield _create_item

    for item in created_items:
        id = item.split(" - ")[1]
        requests.delete(f"{BASE_URL}/api/2/item/{id}")
