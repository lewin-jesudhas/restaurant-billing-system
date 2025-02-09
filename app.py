from flask import Flask, render_template, request, jsonify
from supabase_helpers import add_menu_item, get_menu, place_order, get_orders

app = Flask(__name__)

@app.route('/')
def index():
    menu = get_menu()
    return render_template("index.html", menu=menu)

@app.route('/orders')
def orders():
    orders = get_orders()
    return render_template("orders.html", orders=orders)

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    response = add_menu_item(data["name"], data["price"], data["category"])
    return jsonify(response), 201

@app.route('/place_order', methods=['POST'])
def order():
    data = request.json
    response = place_order(data["items"], data["total_price"])
    return jsonify(response), 201

if __name__ == "__main__":
    app.run(debug=True)
