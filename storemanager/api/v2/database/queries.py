"""The Query module contains all the necessary queries that are used in the application"""
create_category = "INSERT INTO categories(name, description) VALUES(%s, %s) RETURNING id, name, description;"

get_category = "SELECT id, name, description FROM categories WHERE id = %s"

get_category_by_name = "SELECT id, name, description FROM categories WHERE name = %s"

delete_category = "DELETE FROM categories WHERE id = %s"

update_category = "UPDATE categories SET name = %s, description = %s WHERE id = %s"

get_all_categories = "SELECT id, name, description FROM categories ORDER BY id"

create_product = """
INSERT INTO products(name, price, stock, stockmin, description, category) 
VALUES(%s, %s, %s,%s, %s, %s) 
RETURNING id, name, description, price, stock, stockmin, category;"""

get_product = "SELECT id, name, description, price, stock, stockmin, category FROM products WHERE id = %s"
get_product_by_name = "SELECT name FROM products WHERE name = %s"
delete_product = "DELETE FROM products WHERE id = %s"

update_product = """
UPDATE products 
SET name = %s, description = %s, price = %s, stock = %s, stockmin = %s, category = %s 
WHERE id = %s;"""

update_product_after_sale = """
UPDATE products 
SET stock = %s
WHERE id = %s;"""
get_all_products = "SELECT * FROM products ORDER BY id"

create_sale = "INSERT INTO sale_records(items, total) VALUES(%s, %s) RETURNING id, items, total;"

get_sale = "SELECT id, items, total FROM sale_records WHERE id = %s"

get_all_sales = "SELECT id, items, total FROM sale_records ORDER BY id"

create_sale_item = """
INSERT INTO sale_record_items(product_name,price,quantity,total,sale_id) 
VALUES(%s, %s, %s, %s, %s)"""
# RETURNING product_id, price, quantity, total;"""
get_sale_items = "SELECT product_name, price, quantity, total FROM sale_record_items WHERE sale_id = %s ORDER BY id"

create_user = "INSERT INTO users(name, password,role) VALUES(%s, %s, %s) RETURNING id, name, role;"

get_user = "SELECT id, name, role FROM users WHERE id = %s"

get_user_by_name = "SELECT id, name, password, role FROM users WHERE name = %s"

delete_user = "DELETE FROM users WHERE id = %s"

update_user = "UPDATE users SET name = %s, password = %s WHERE id = %s"

get_all_users = "SELECT id, name, role FROM users ORDER BY id"
