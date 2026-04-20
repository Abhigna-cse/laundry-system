from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# ── In-memory storage ──────────────────────────────────────────────────
orders = {}

# ── Price list ─────────────────────────────────────────────────────────
PRICE_LIST = {
    "shirt":    50,
    "pants":    60,
    "saree":   120,
    "jacket":  150,
    "kurta":    70,
    "suit":    200,
    "bedsheet":100,
    "blanket": 180,
    "towel":    40,
}

VALID_STATUSES = ["RECEIVED", "PROCESSING", "READY", "DELIVERED"]

# ── Helper ─────────────────────────────────────────────────────────────
def calculate_bill(garments):
    total = 0
    for item in garments:
        name  = item.get("name", "").lower()
        qty   = item.get("quantity", 1)
        price = item.get("price") or PRICE_LIST.get(name, 50)
        item["price"] = price
        item["subtotal"] = price * qty
        total += item["subtotal"]
    return total

# ══════════════════════════════════════════════════════════════════════
#  FRONTEND
# ══════════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template("index.html")

# ══════════════════════════════════════════════════════════════════════
#  1. CREATE ORDER   POST /orders
# ══════════════════════════════════════════════════════════════════════
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name     = data.get("customer_name", "").strip()
    phone    = data.get("phone", "").strip()
    garments = data.get("garments", [])

    if not name:
        return jsonify({"error": "customer_name is required"}), 400
    if not phone:
        return jsonify({"error": "phone is required"}), 400
    if not garments:
        return jsonify({"error": "garments list is required"}), 400

    order_id   = "ORD-" + str(uuid.uuid4())[:8].upper()
    total_bill = calculate_bill(garments)
    created_at = datetime.now()
    estimated_delivery = created_at + timedelta(days=2)

    order = {
        "order_id":           order_id,
        "customer_name":      name,
        "phone":              phone,
        "garments":           garments,
        "total_bill":         total_bill,
        "status":             "RECEIVED",
        "created_at":         created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d"),
        "updated_at":         created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    orders[order_id] = order

    return jsonify({
        "message":   "Order created successfully",
        "order_id":  order_id,
        "total_bill": total_bill,
        "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d"),
        "order":     order,
    }), 201

# ══════════════════════════════════════════════════════════════════════
#  2. UPDATE STATUS   PATCH /orders/<id>/status
# ══════════════════════════════════════════════════════════════════════
@app.route("/orders/<order_id>/status", methods=["PATCH"])
def update_status(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404

    data       = request.get_json()
    new_status = data.get("status", "").upper()

    if new_status not in VALID_STATUSES:
        return jsonify({
            "error": f"Invalid status. Choose from {VALID_STATUSES}"
        }), 400

    orders[order_id]["status"]     = new_status
    orders[order_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "message":  "Status updated",
        "order_id": order_id,
        "status":   new_status,
    })

# ══════════════════════════════════════════════════════════════════════
#  3. VIEW ALL ORDERS   GET /orders
#     Filter: ?status=READY  or  ?search=John  or  ?garment=saree
# ══════════════════════════════════════════════════════════════════════
@app.route("/orders", methods=["GET"])
def get_orders():
    status_filter  = request.args.get("status", "").upper()
    search_filter  = request.args.get("search", "").lower()
    garment_filter = request.args.get("garment", "").lower()

    result = list(orders.values())

    if status_filter:
        result = [o for o in result if o["status"] == status_filter]

    if search_filter:
        result = [
            o for o in result
            if search_filter in o["customer_name"].lower()
            or search_filter in o["phone"]
        ]

    if garment_filter:
        result = [
            o for o in result
            if any(garment_filter in g["name"].lower() for g in o["garments"])
        ]

    return jsonify({"total": len(result), "orders": result})

# ══════════════════════════════════════════════════════════════════════
#  4. GET SINGLE ORDER   GET /orders/<id>
# ══════════════════════════════════════════════════════════════════════
@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(orders[order_id])

# ══════════════════════════════════════════════════════════════════════
#  5. DASHBOARD   GET /dashboard
# ══════════════════════════════════════════════════════════════════════
@app.route("/dashboard", methods=["GET"])
def dashboard():
    all_orders     = list(orders.values())
    total_orders   = len(all_orders)
    total_revenue  = sum(o["total_bill"] for o in all_orders)

    orders_per_status = {s: 0 for s in VALID_STATUSES}
    for o in all_orders:
        orders_per_status[o["status"]] += 1

    return jsonify({
        "total_orders":       total_orders,
        "total_revenue":      total_revenue,
        "orders_per_status":  orders_per_status,
        "price_list":         PRICE_LIST,
    })

# ══════════════════════════════════════════════════════════════════════
#  6. DELETE ORDER   DELETE /orders/<id>
# ══════════════════════════════════════════════════════════════════════
@app.route("/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404
    del orders[order_id]
    return jsonify({"message": f"Order {order_id} deleted"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
