from flask import abort


class CustomValidator:

    @staticmethod
    def validate_register_details(username, password, role):
        # validation checks for username
        if username.isdigit():
            abort(400, 'username cannot be an integer value')
        if not username or username.isspace():
            abort(400, 'please provide a username')

        # validation checks for password
        if not password or password.isspace():
            abort(400, 'please provide a password')

        # validation checks for product name
        if role.isdigit():
            abort(400, 'user role cannot be an integer value')
        if not role or role.isspace():
            abort(400, 'user role required, should not be empty')

    @staticmethod
    def validate_login_details(username, password):
        # validation checks for username
        if username.isdigit():
            abort(400, 'username cannot be an integer value')
        if not username or username.isspace():
            abort(400, 'please provide a username')

        # validation checks for password
        if not password or password.isspace():
            abort(400, 'please provide a password')

    @staticmethod
    def validate_product_details(p_name, p_price, p_desc, p_cat, p_stock, p_min_stock):
        # validation checks for product name
        if p_name.isdigit():
            abort(400, 'name cannot be an integer value')
        if not p_name or p_name.isspace():
            abort(400, 'name should not be empty')

        # validation checks for product price
        if p_price < 0:
            abort(400, 'price cannot be a negative or 0')

        # validation checks for product description
        if p_desc.isdigit():
            abort(400, 'description cannot be an integer value')
        if not p_desc or p_desc.isspace():
            abort(400, 'description should not be empty')

        # validation checks for product category
        if p_cat.isdigit():
            abort(400, 'category cannot be an integer value')
        if not p_cat or p_cat.isspace():
            abort(400, 'category should not be empty')

        # validation checks for product stock
        if p_stock < 0:
            abort(400, 'stock cannot be a negative or 0')

        # validation checks for product minimum stock
        if p_min_stock < 0:
            abort(400, 'minimum cannot be a negative or 0')

    @staticmethod
    def validate_category_details(c_name, c_desc):
        if c_name.isdigit():
            abort(400, 'name cannot be an integer value')
        if not c_name or c_name.isspace():
            abort(400, 'please provide a category name')
        if c_desc.isdigit():
            abort(400, 'description cannot be an integer value')

    @staticmethod
    def validate_sale_items(p_name, p_count):
        if p_name.isdigit():
            abort(400, 'name cannot be an integer value')

        if p_count < 0:
            abort(400, 'product count cannot be negative')

        if p_count == 0:
            abort(400, 'product count must be 1 and above')
