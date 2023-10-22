CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    password TEXT,
    position TEXT
);
CREATE TABLE Suppliers (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    address TEXT
);
CREATE TABLE Warehouses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);
CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    manufacturer TEXT,
    description TEXT,
    price INTEGER
);
CREATE TABLE Inventory_item (
    id SERIAL PRIMARY KEY,
    unit_size INTEGER,
    product_id INTEGER REFERENCES Products,
    supplier_id INTEGER REFERENCES Suppliers,
    location_id INTEGER REFERENCES Warehouses
);
CREATE TABLE Purchases (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER REFERENCES Suppliers
);
CREATE TABLE Customers (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    address TEXT
);
CREATE TABLE Sales (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES Customers,
    sale_date TIMESTAMP,
    address TEXT,
    sales_person_id INTEGER,
    total_amount INTEGER
);
CREATE TABLE Salesdetail (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES Sales,
    product_id INTEGER REFERENCES Products,
    quantity INTEGER,
    from_warehouse INTEGER REFERENCES Warehouses
)
