"""The Query module contains all the necessary queries that are used in the application"""

CREATE_TABLE_USERS = """
    CREATE TABLE USERS (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    ROLE VARCHAR(10) NOT NULL,
    PASSWORD VARCHAR(60) NOT NULL
    );"""

CREATE_TABLE_CATEGORIES = """
    CREATE TABLE CATEGORIES (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    DESCRIPTION TEXT
    );"""

CREATE_TABLE_PRODUCTS = """
    CREATE TABLE PRODUCTS (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    PRICE INTEGER NOT NULL,
    STOCK INTEGER NOT NULL,
    STOCKMIN INTEGER NOT NULL,
    DESCRIPTION TEXT NOT NULL,
    CATEGORY INTEGER REFERENCES CATEGORIES (ID)
    );"""

CREATE_TABLE_SALES = """
    CREATE TABLE SALE_RECORDS (
    ID SERIAL PRIMARY KEY,
    ITEMS INTEGER NOT NULL,
    TOTAL INTEGER NOT NULL
    );"""

CREATE_TABLE_SALE_ITEMS = """
    CREATE TABLE SALE_RECORD_ITEMS (
    ID SERIAL PRIMARY KEY,
    PRODUCT_NAME TEXT NOT NULL,
    PRICE INTEGER NOT NULL,
    QUANTITY INTEGER NOT NULL,
    TOTAL INTEGER NOT NULL,
    SALE_ID INTEGER REFERENCES SALE_RECORDS (ID)
    );"""

DROP_ALL_TABLES = """
    DROP TABLE IF EXISTS USERS, PRODUCTS, CATEGORIES, SALE_RECORDS, SALE_RECORD_ITEMS;"""

CREATE_CATEGORY = """
    INSERT INTO categories(name, description) 
    VALUES(%s, %s) 
    RETURNING id, name, description;"""

GET_CATEGORY = """
    SELECT id, name, description 
    FROM categories 
    WHERE id = %s"""

GET_CATEGORY_BY_NAME = """
    SELECT id, name, description 
    FROM categories 
    WHERE name = %s"""

DELETE_CATEGORY = """
    DELETE FROM categories 
    WHERE id = %s"""

UPDATE_CATEGORY = """
    UPDATE categories 
    SET name = %s, description = %s 
    WHERE id = %s"""

GET_ALL_CATEGORIES = """
    SELECT id, name, description 
    FROM categories 
    ORDER BY id"""

CREATE_PRODUCT = """
    INSERT INTO products(name, price, stock, stockmin, description, category) 
    VALUES(%s, %s, %s,%s, %s, %s) 
    RETURNING id, name, description, price, stock, stockmin, category;"""

GET_PRODUCT = """
    SELECT * FROM products 
    WHERE id = %s"""

GET_PRODUCT_BY_NAME = """
    SELECT id, name, price, stock, stockmin 
    FROM products 
    WHERE name = %s"""

DELETE_PRODUCT = """
    DELETE FROM products 
    WHERE id = %s"""

UPDATE_PRODUCT = """
    UPDATE products 
    SET name = %s, description = %s, price = %s, stock = %s, stockmin = %s, category = %s 
    WHERE id = %s;"""

UPDATE_PRODUCT_ON_SALE = """
    UPDATE products 
    SET stock = %s
    WHERE id = %s;"""

GET_ALL_PRODUCTS = """
    SELECT * FROM products ORDER BY id"""

CREATE_SALE = """
    INSERT INTO sale_records(items, total) 
    VALUES(%s, %s) 
    RETURNING id, items, total;"""

GET_SALE = """
    SELECT id, items, total 
    FROM sale_records 
    WHERE id = %s"""

GET_ALL_SALES = """
    SELECT id, items, total 
    FROM sale_records 
    ORDER BY id"""

CREATE_SALE_ITEM = """
    INSERT INTO sale_record_items(product_name,price,quantity,total,sale_id) 
    VALUES(%s, %s, %s, %s, %s)"""
# RETURNING product_id, price, quantity, total;"""

GET_SALE_ITEMS = """
    SELECT product_name, price, quantity, total 
    FROM sale_record_items 
    WHERE sale_id = %s 
    ORDER BY id"""

CREATE_USER = """
    INSERT INTO users(name, password,role) 
    VALUES(%s, %s, %s) 
    RETURNING id, name, role;"""

GET_USER = """
    SELECT id, name, role 
    FROM users 
    WHERE id = %s"""

GET_USER_BY_NAME = """
    SELECT id, name, password, role 
    FROM users 
    WHERE name = %s"""

DELETE_USER = """
    DELETE FROM users 
    WHERE id = %s"""

UPDATE_USER = """
    UPDATE users 
    SET name = %s, password = %s 
    WHERE id = %s"""

GET_ALL_USERS = """
    SELECT id, name, role 
    FROM users 
    ORDER BY id"""
