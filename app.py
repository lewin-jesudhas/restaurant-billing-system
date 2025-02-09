from flask import Flask, render_template, request, jsonify
from supabase_helpers import get_menu, update_cart, place_order, order_confirm

app = Flask(__name__)

@app.route('/')
def index():
    menu = get_menu()  # Fetch menu items from Supabase
    #print(menu)
    return render_template("index.html", menu=menu)

@app.route('/update_cart', methods=['POST'])
def update_cart_route():
    data = request.json
    item_name = data["name"]
    quantity = data["quantity"]

    response = update_cart(item_name, quantity)
    return jsonify(response), 200

@app.route('/place_order', methods=['POST'])
def order():
    data = request.json
    total_price = data["total_price"]
    items = data["items"]

    response = place_order(items, total_price)
    return jsonify(response), 201

@app.route('/order_summary')
def order_summary():
    return render_template("order_summary.html")

# @app.route('/confirm_order', methods=['POST'])
# def confirm_order():
#     data = request.json
#     print("Order Confirmed:", data)  # You can save this to a database
#     return {"status": "success", "message": "Order placed successfully!"}

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    try:
        data = request.json  # Get JSON data from frontend
        items = data.get("items", [])
        total_price = float(data.get("total_price", 0))
        payment_type = data.get("payment_method", "Cash")
        response = order_confirm(items,total_price,payment_type)
        return jsonify({"status": "success", "message": "Order placed successfully!", "data": response.data})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
