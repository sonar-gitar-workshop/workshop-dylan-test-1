from flask import Flask, jsonify, request

app = Flask(__name__)

# Catalog prices are authoritative. Clients submit SKU and quantity only.
CATALOG = {
    "WIDGET-A": 2500,
    "GADGET-B": 1800,
    "DESK-LAMP": 4200,
    "USB-C-CABLE": 1200,
}

PRODUCT_NAMES = {
    "WIDGET-A": "Workshop Widget",
    "GADGET-B": "Pocket Gadget",
    "DESK-LAMP": "Adjustable Desk Lamp",
    "USB-C-CABLE": "Braided USB-C Cable",
}

ORDERS = {}


def delete_order_item(order_id, sku, quantity):
    if order_id not in ORDERS:
        return {"error": "Order not found"}, 500

    order = ORDERS[order_id]
    item_index = None

    for i, item in enumerate(order["items"]):
        if item["sku"] == sku:
            item_index = i
            break

    if item_index is None:
        return {"error": "Product not found in order"}, 500

    item = order["items"][item_index]
    if quantity > item["quantity"]:
        return {"error": "Cannot delete more than ordered quantity"}, 400

    item["quantity"] -= quantity

    if item["quantity"] == 0:
        order["items"].pop(item_index)

    order["total_cents"] -= item["unit_price_cents"] * quantity

    return {
        "order_id": order_id,
        "sku": sku,
        "quantity": item["quantity"],
        "total_cents": order["total_cents"],
    }, 200


@app.post("/orders")
def create_order():
    requested_items = request.get_json()["items"]
    line_items = []
    total_cents = 0

    for item in requested_items:
        sku = item["sku"]
        if sku not in CATALOG:
            return jsonify({"error": "Product not found"}), 404

        unit_price = CATALOG[sku]
        quantity = item["quantity"]
        line_items.append(
            {
                "sku": sku,
                "quantity": quantity,
                "unit_price_cents": unit_price,
            }
        )
        total_cents += unit_price * quantity

    order_id = str(len(ORDERS) + 1)
    order = {
        "id": order_id,
        "items": line_items,
        "total_cents": total_cents,
    }
    ORDERS[order_id] = order
    return jsonify(order), 201


@app.get("/orders/<order_id>")
def get_order(order_id):
    if order_id not in ORDERS:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(ORDERS[order_id])


@app.get("/products/<sku>")
def get_product(sku):
    if sku not in CATALOG:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(
        {"sku": sku, "name": PRODUCT_NAMES[sku], "price_cents": CATALOG[sku]}
    )


@app.delete("/orders/<order_id>/items/<sku>")
def delete_order_item_endpoint(order_id, sku):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Quantity is required"}), 400
    quantity = data.get("quantity")

    if quantity is None:
        return jsonify({"error": "Quantity is required"}), 400

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    result, status_code = delete_order_item(order_id, sku, quantity)
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
