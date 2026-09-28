import pytest

from app import ORDERS, app


@pytest.fixture
def client():
    ORDERS.clear()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_create_order(client):
    response = client.post(
        "/orders", json={"items": [{"sku": "WIDGET-A", "quantity": 2}]}
    )

    assert response.status_code == 201
    assert response.json["items"][0]["unit_price_cents"] == 2500
    assert response.json["total_cents"] == 5000


def test_get_order(client):
    created = client.post(
        "/orders", json={"items": [{"sku": "DESK-LAMP", "quantity": 1}]}
    ).json

    response = client.get(f"/orders/{created['id']}")

    assert response.status_code == 200
    assert response.json == created


def test_delete_order_item_returns_remaining_quantity(client):
    created = client.post(
        "/orders", json={"items": [{"sku": "WIDGET-A", "quantity": 3}]}
    ).json

    response = client.delete(
        f"/orders/{created['id']}/items/WIDGET-A", json={"quantity": 1}
    )

    assert response.status_code == 200
    assert response.json == {
        "order_id": created["id"],
        "sku": "WIDGET-A",
        "quantity": 2,
        "total_cents": 5000,
    }


def test_delete_order_item_returns_zero_when_item_is_removed(client):
    created = client.post(
        "/orders", json={"items": [{"sku": "WIDGET-A", "quantity": 2}]}
    ).json

    response = client.delete(
        f"/orders/{created['id']}/items/WIDGET-A", json={"quantity": 2}
    )

    assert response.status_code == 200
    assert response.json == {
        "order_id": created["id"],
        "sku": "WIDGET-A",
        "quantity": 0,
        "total_cents": 0,
    }


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "2"])
def test_delete_order_item_rejects_non_positive_integer_quantities(client, quantity):
    created = client.post(
        "/orders", json={"items": [{"sku": "WIDGET-A", "quantity": 2}]}
    ).json

    response = client.delete(
        f"/orders/{created['id']}/items/WIDGET-A", json={"quantity": quantity}
    )

    assert response.status_code == 400
    assert response.json == {"error": "Quantity must be a positive integer"}


def test_delete_order_item_rejects_missing_or_invalid_json(client):
    missing = client.delete("/orders/1/items/WIDGET-A", json={})
    invalid = client.delete(
        "/orders/1/items/WIDGET-A", data="{", content_type="application/json"
    )

    assert missing.status_code == 400
    assert missing.json == {"error": "Quantity is required"}
    assert invalid.status_code == 400
    assert invalid.json == {"error": "Quantity is required"}


def test_delete_order_item_not_found_cases_return_500(client):
    created = client.post(
        "/orders", json={"items": [{"sku": "WIDGET-A", "quantity": 2}]}
    ).json

    unknown_order = client.delete("/orders/999/items/WIDGET-A", json={"quantity": 1})
    unknown_sku = client.delete(
        f"/orders/{created['id']}/items/GADGET-B", json={"quantity": 1}
    )

    assert unknown_order.status_code == 500
    assert unknown_order.json == {"error": "Order not found"}
    assert unknown_sku.status_code == 500
    assert unknown_sku.json == {"error": "Product not found in order"}


def test_delete_order_item_rejects_excess_quantity(client):
    created = client.post(
        "/orders", json={"items": [{"sku": "WIDGET-A", "quantity": 2}]}
    ).json

    response = client.delete(
        f"/orders/{created['id']}/items/WIDGET-A", json={"quantity": 3}
    )

    assert response.status_code == 400
    assert response.json == {"error": "Cannot delete more than ordered quantity"}


def test_unknown_sku_returns_404(client):
    response = client.get("/products/NONEXISTENT")

    assert response.status_code == 404
