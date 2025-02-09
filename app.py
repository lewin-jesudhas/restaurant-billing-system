from flask import Flask, render_template, request, jsonify
from supabase_helpers import get_menu, update_cart, place_order

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

if __name__ == '__main__':
    app.run(debug=True)
