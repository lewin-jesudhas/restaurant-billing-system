from flask import Flask, render_template, request, jsonify
from supabase_helpers import get_menu, update_cart, place_order, order_confirm
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Set frontend URL in production

@app.route('/')
def index():
    try:
        menu = get_menu()  # Fetch menu items from Supabase
        return render_template("index.html", menu=menu)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update_cart', methods=['POST'])
def update_cart_route():
    try:
        data = request.json
        item_name = data.get("name")
        quantity = data.get("quantity", 1)
        if not item_name:
            return jsonify({"status": "error", "message": "Item name is required"}), 400
        response = update_cart(item_name, quantity)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/place_order', methods=['POST'])
def order():
    try:
        data = request.json
        total_price = float(data.get("total_price", 0))
        items = data.get("items", [])

        if not items:
            return jsonify({"status": "error", "message": "Order items cannot be empty"}), 400

        response = place_order(items, total_price)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/order_summary')
def order_summary():
    return render_template("order_summary.html")

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    try:
        data = request.json
        items = data.get("items", [])
        total_price = float(data.get("total_price", 0))
        payment_type = data.get("payment_method", "Cash")

        if not items:
            return jsonify({"status": "error", "message": "No items in order"}), 400

        response = order_confirm(items, total_price, payment_type)
        return jsonify({"status": "success", "message": "Order placed successfully!", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Remove app.run() since Gunicorn will handle this in production
