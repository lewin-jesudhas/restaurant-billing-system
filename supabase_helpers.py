# from config import supabase

# def add_menu_item(name, price, category):
#     response = supabase.table("menu").insert({
#         "name": name,
#         "price": price,
#         "category": category
#     }).execute()
#     return response

# def get_menu():
#     response = supabase.table("menu").select("*").execute()
#     return response.data

# def place_order(items, total_price):
#     response = supabase.table("orders").insert({
#         "items": items,
#         "total_price": total_price,
#         "status": "Pending"
#     }).execute()
#     return response

# def get_orders():
#     response = supabase.table("orders").select("*").execute()
#     return response.data


from config import supabase

def get_menu():
    """Fetch menu items from the database."""
    response = supabase.table("menu").select("*").execute()
    return response.data

def update_cart(item_name, quantity):
    """Updates the quantity of an item in the cart."""
    data, count = supabase.table("cart").upsert({
        "name": item_name,
        "quantity": quantity
    }).execute()
    
    return {"status": "success", "updated_item": item_name, "quantity": quantity}

def place_order(items, total_price):
    """Stores the order details in the database."""
    data, _ = supabase.table("orders").insert({
        "items": items,
        "total_price": total_price
    }).execute()
    
    return {"status": "success", "order": data}

def order_confirm(items, total_price, payment_type, customer_name, customer_phone):
    response = supabase.table("orders").insert({
        "items": items,
        "total_price": total_price,
        "payment_type": payment_type,
        "customer_name": customer_name,
        "customer_phone": customer_phone
    }).execute()
    return response  # Return the response



def get_user_credentials(username):
    """Fetch stored hashed password for a given username."""
    response = supabase.table("users").select("username, password").eq("username", username).single().execute()

    if response.data:
        return response.data  # Returns {'username': 'Rohan', 'password': 'hashed_pw'}
    return None
