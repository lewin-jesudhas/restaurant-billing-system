from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from supabase_helpers import get_menu, update_cart, place_order, order_confirm, get_user_credentials
from flask_cors import CORS
import os
from flask_bcrypt import Bcrypt
from config import supabase

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)  # Session security
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session expiry time

bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": ["https://restaurant-billing-system-production.up.railway.app"]}})


@app.route("/", methods=["GET", "POST"])
def login():
    """Handles user login"""
    if request.method == "POST":
        data = request.json
        username = data.get("username")
        password = data.get("password").encode("utf-8")  # Convert input to bytes

        # Fetch user from Supabase
        user = get_user_credentials(username)

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = username  # Store in session
            #base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000")  # Fallback to localhost if not set
            return jsonify({"status": "success", "redirect": f"/menu"}), 200

        return jsonify({"status": "error", "message": "Invalid username or password"}), 401

    return render_template("login.html")


@app.route("/menu")
def menu_page():
    """Fetch menu items from Supabase"""
    if "user" not in session:  # Ensure user is logged in
        return redirect(url_for("login"))

    menu = get_menu()
    return render_template("index.html", menu=menu)


@app.route("/logout")
def logout():
    """Logout and clear session"""
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/update_cart", methods=["POST"])
def update_cart_route():
    if "user" not in session:
        return redirect(url_for("login"))

    data = request.json
    item_name = data["name"]
    quantity = data["quantity"]

    response = update_cart(item_name, quantity)
    return jsonify(response), 200


@app.route("/place_order", methods=["POST"])
def order():
    if "user" not in session:
        return redirect(url_for("login"))

    data = request.json
    total_price = data["total_price"]
    items = data["items"]

    response = place_order(items, total_price)
    return jsonify(response), 201


@app.route('/order_summary')
def order_summary():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("order_summary.html")


@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        data = request.json
        items = data.get("items", [])
        total_price = float(data.get("total_price", 0))
        payment_type = data.get("payment_method", "Cash")
        response = order_confirm(items, total_price, payment_type)
        return jsonify({"status": "success", "message": "Order placed successfully!", "data": response.data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/orders")
def get_orders():
    if "user" not in session:
        return redirect(url_for("login"))

    response = supabase.table("orders").select("*").execute()
    orders = response.data

    # Debugging - print structure to confirm
    #print("Fetched Orders:", orders)

    # Ensure 'items' is converted to a list
    for order in orders:
        if isinstance(order.get("items"), str):  # Check if items are stored as JSON strings
            order["items"] = eval(order["items"])  # Convert string to list (use json.loads() if JSON formatted)

    return render_template("orders.html", orders=orders)


@app.route("/complete_order", methods=["POST"])
def complete_order():
    order_id = request.json.get("order_id")
    if order_id:
        response = supabase.table("orders").update({"status": "complete"}).eq("id", order_id).execute()
        if response.data:
            return jsonify({"message": "Order marked as complete"}), 200
        return jsonify({"error": "Failed to update order"}), 400
    return jsonify({"error": "Invalid order ID"}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
