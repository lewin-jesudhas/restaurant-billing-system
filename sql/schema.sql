CREATE TABLE public.menu (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    price FLOAT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE public.orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    items JSONB NOT NULL,  -- Stores list of ordered items
    total_price FLOAT NOT NULL,
    payment_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);


INSERT INTO public.menu (name, price, category) 
VALUES 
('Chicken Taco', 60, 'Taco'),
('Veggie Taco', 45, 'Taco'),
('Coke', 15, 'Drink'),
('Coke McFloat', 35, 'Drink'),
('Ice Cream', 20, 'Dessert'),
('Brownie', 40, 'Dessert');
