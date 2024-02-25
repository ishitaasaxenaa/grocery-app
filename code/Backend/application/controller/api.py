from application.data.models import User, Role, Category, Product, Cart, CartItem, CategoryApprove,ManagerApproval
from application.data.database import db
from application.data.data_access import get_all_products
from flask_security import SQLAlchemyUserDatastore, Security, hash_password,current_user
from flask_security import RegisterForm, auth_required, roles_required
from flask_security.registerable import register_user
from wtforms import StringField 
from flask_restful import Api, Resource, reqparse
from flask import request
from application.jobs import tasks

class ExtendedRegisterForm(RegisterForm):
    role = StringField('Role')

class registerApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        user = user_datastore.create_user(email=args['email'], username=args['username'], password=hash_password(args['password']))
        role = "user"
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
        return "User registered successfully and assigned to role", 200

class AssignRoleApi(Resource):
    @auth_required("token")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        email = args['email']
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        
        # Find the user by email using an SQLAlchemy query
        user = db.session.query(User).filter_by(email=email).first()
        
        if user:
            # Assign the role to the user
            user_datastore.add_role_to_user(user, "user")
            db.session.commit()
            return "Role assigned to the user"
        else:
            return "User not found", 404

class CategoryApi(Resource):
    @auth_required('token', 'session')
    def get(self):
        category_id = request.args.get('id')
        if category_id:
            category = Category.query.get(category_id)
            if category:
                return {
                    'id': category.id,
                    'name': category.name
                }, 200
            else:
                return "Category not found", 404
        else:
            categories = Category.query.all()
            result = []
            for category in categories:
                result.append({
                    'id': category.id,
                    'name': category.name
                })
            return result, 200

    @auth_required('token', 'session')
    @roles_required('admin')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        category = Category(name=args['name'])
        db.session.add(category)
        db.session.commit()
        return "Category added successfully", 201
    
    @auth_required('token', 'session')
    @roles_required('admin')
    def delete(self):
        category_id = request.args.get('id')
        if category_id:
            category = Category.query.get(category_id)
            if category:
                db.session.delete(category)
                db.session.commit()
                return "Category deleted successfully", 200
            else:
                return "Category not found", 404
        else:
            return "No category id provided", 400
        
    @auth_required('token', 'session')
    @roles_required('admin')
    def put(self):
        category_id = request.args.get('id')
        new_name = request.args.get('name')
        if category_id and new_name:
            category = Category.query.get(category_id)
            if category:
                category.name = new_name
                db.session.commit()
                return "Category updated successfully", 200
            else:
                return "Category not found", 404
        else:
            return "No category id or new name provided", 400

class ProductApi(Resource):
    @auth_required('token', 'session')
    def get(self):
        product_id = request.args.get('id')
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return {
                    'id': product.id,
                    'name': product.name,
                    'category_id': product.category_id,
                    'price': product.price,
                    'quantity': product.quantity,
                    'unit': product.unit
                }, 200
            else:
                return "Product not found", 404

    @auth_required('token', 'session')
    @roles_required('manager')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('category_id', type=int, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('quantity', type=int, required=True)
        parser.add_argument('unit', type=str, required=True)
        args = parser.parse_args()

        product = Product(name=args['name'], category_id=args['category_id'], price=args['price'], quantity=args['quantity'], unit=args['unit'])
        db.session.add(product)
        db.session.commit()
        return "Product added successfully", 201

    @auth_required('token', 'session')
    @roles_required('manager')
    def delete(self):
        product_id = request.args.get('id')
        if product_id:
            product = Product.query.get(product_id)
            if product:
                db.session.delete(product)
                db.session.commit()
                return "Product deleted successfully", 200
            else:
                return "Product not found", 404
        else:
            return "No product id provided", 400

    @auth_required('token', 'session')
    @roles_required('manager')
    def put(self):
        product_id = request.args.get('id')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('category_id', type=int)
        parser.add_argument('price', type=int)
        parser.add_argument('quantity', type=int)
        parser.add_argument('unit', type=str)
        args = parser.parse_args()

        if product_id:
            product = Product.query.get(product_id)
            if product:
                product.name = args.get('name', product.name)
                product.category_id = args.get('category_id', product.category_id)
                product.price = args.get('price', product.price)
                product.quantity = args.get('quantity', product.quantity)
                product.unit = args.get('unit', product.unit)
                db.session.commit()
                return "Product updated successfully", 200
            else:
                return "Product not found", 404
        else:
            return "No product id provided", 400

class GetAllProduct(Resource):
    # @auth_required("token")
    def get(self):
        # result = get_all_products()
        products = Product.query.all()
        result = []
        for product in products:
            category = Category.query.get(product.category_id)
            product_dict = {
                'id': product.id,
                'name': product.name,
                'category': category.name if category else None,
                'category_id': product.category_id,
                'price': product.price,
                'quantity': product.quantity,
                'unit': product.unit
            }
            result.append(product_dict)
        return result, 200

class getCachedProducts(Resource):
    def get(self):
        result = get_all_products()
        return result, 200

class CartApi(Resource):
    @auth_required('token', 'session')
    def get(self):
        try:
            user_id = current_user.id
            cart = Cart.query.filter_by(user_id=user_id).first()

            if not cart:
                return {'message': 'Cart not found.'}, 404

            cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()

            products_in_cart = []
            for cart_item in cart_items:
                product = Product.query.get(cart_item.product_id)
                cart_item_id = cart_item.cart_item_id
                cart_id = cart_item.cart_id 
                if product:
                    products_in_cart.append({
                        'cart_item_id': cart_item_id,
                        'product_id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'quantity': cart_item.quantity,
                        'cart_id': cart_id
                    })

            return {'products_in_cart': products_in_cart}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error.'}, 500
        
    @auth_required('token', 'session')
    def post(self):
        try:
            user_id = current_user.id  
            data = request.get_json()
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            if not (product_id and quantity):
                return {'message': 'Product ID and quantity are required.'}, 400

            cart = Cart.query.filter_by(user_id=user_id).first()
            if not cart:
                cart = Cart(user_id=user_id)
                db.session.add(cart)

            cart_item = CartItem(cart_id=cart.cart_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

            db.session.commit()

            return {'message': 'Product added to the cart successfully.'}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error.'}, 500
    
    @auth_required('token', 'session')
    def delete(self):
        try:
            cart_item_id = request.args.get('cart_item_id')
            cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id).first()
            if not cart_item:
                return {'message': 'Product not found in the cart.'}, 404

            db.session.delete(cart_item)
            db.session.commit()

            return {'message': 'Product deleted from the cart successfully.'}, 200
        
        except Exception as e: 
            print(e)
            return {'message': 'Internal Server Error.'}, 500

class CheckRoleApi(Resource):
    @auth_required('token', 'session')  
    def get(self):
        user_id = current_user.id
        role_id = current_user.roles[-1].id
        return role_id, 200
    
    @auth_required('token', 'session')
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        role = data.get('role')
        if user_id and role:
            user = User.query.get(user_id)
            if user:
                user_datastore = SQLAlchemyUserDatastore(db, User, Role)
                user_datastore.add_role_to_user(user, role)
                db.session.commit()
                return "Role assigned to the user", 200
            else:
                return "User not found", 404
        else:
            return "No user id or role provided", 400

class SearchApi(Resource):
    @auth_required('token', 'session')
    def get(self):
        keyword = request.args.get('q')
        max_price = request.args.get('max_price',type = int)
        if keyword:
            products = Product.query.filter(Product.name.like('%' + keyword + '%')).all()
            categories = Category.query.filter(Category.name.like('%' + keyword + '%')).all()
            result = []
            if products is not None:
                for product in products:
                    category = Category.query.get(product.category_id)
                    product_dict = {
                        'id': product.id,
                        'name': product.name,
                        'category': category.name if category else None,
                        'category_id': product.category_id,
                        'price': product.price,
                        'quantity': product.quantity,
                        'unit': product.unit
                    }
                    result.append(product_dict)
            if categories is not None:
                cat = []
                for category in categories:
                    category_dict = {
                        'id': category.id,
                        'name': category.name
                    }
                    cat.append(category_dict)
                    for category in cat:
                        products = Product.query.filter(Product.category_id == category['id']).all()
                        for product in products:
                            category = Category.query.get(product.category_id)
                            product_dict = {
                                'id': product.id,
                                'name': product.name,
                                'category': category.name if category else None,
                                'category_id': product.category_id,
                                'price': product.price,
                                'quantity': product.quantity,
                                'unit': product.unit
                            }
                            result.append(product_dict)
            seen_ids = set()

            unique_data = []

            for item in result:
                if item["id"] not in seen_ids:
                    seen_ids.add(item["id"])
                    unique_data.append(item)

            result = unique_data
            for product in result:
                if max_price:
                    if product['price'] > max_price:
                        result.remove(product)
            return result, 200
        else:
            return "No keyword provided", 400
        
class CategoryApproveApi(Resource):
    @auth_required('token', 'session')
    @roles_required('manager')
    def post(self):
        data = request.get_json()
        category = CategoryApprove(name=data.get('name'), action = data.get('action'), categoryid = data.get('categoryid'))
        db.session.add(category)
        db.session.commit()
        return "Category added successfully", 201

    @auth_required('token', 'session')
    @roles_required('admin')
    def get(self):
        category_id = request.args.get('id')
        if category_id:
            category = CategoryApprove.query.get(category_id)
            if category:
                return {
                    'id': category.id,
                    'name': category.name,
                    'action': category.action,
                    'categoryid': category.categoryid
                }, 200
            else:
                return "Category not found", 404
        else:
            categories = CategoryApprove.query.all()
            result = []
            for category in categories:
                result.append({
                    'id': category.id,
                    'name': category.name,
                    'action': category.action,
                    'categoryid': category.categoryid
                })
            return result, 200
    
    @auth_required('token', 'session')
    @roles_required('admin')
    def delete(self):
        category_id = request.args.get('id')
        if category_id:
            category = CategoryApprove.query.get(category_id)
            if category:
                db.session.delete(category)
                db.session.commit()
                return "Category deleted successfully", 200
            else:
                return "Category not found", 404
        else:
            return "No category id provided", 400

class callCeleryApi(Resource):
    @auth_required('token', 'session')
    # @roles_required('manager')
    def get(self):
        tasks.send_mail_task()
        return "mail sent successfully", 200

class sendCsvApi(Resource):
    @auth_required('token', 'session')
    @roles_required('manager')
    def get(self):
        user = current_user
        email = user.email
        user_id = user.id
        tasks.send_products(email,user_id)
        return "mail sent successfully", 200   

class sendBarPlotPdf(Resource):

    @auth_required('token', 'session')
    @roles_required('manager')
    def get(self):
        user = current_user
        tasks.send_bar_plot_pdf_task(user.email,user.id)
        return "mail sent successfully", 200
    
class buyAll(Resource):
    @auth_required('token', 'session')
    def get(self):
        user_id = current_user.id
        cart = Cart.query.filter_by(user_id=user_id).first()
        cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
        products_in_cart = []
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            cart_item_id = cart_item.cart_item_id
            if product:
                products_in_cart.append({
                    'cart_item_id': cart_item_id,
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': cart_item.quantity,
                })
        for product in products_in_cart:
            product_id = product['product_id']
            quantity = product['quantity']
            product = Product.query.get(product_id)
            product.quantity -= quantity
            db.session.commit()
        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
        return "Products bought successfully", 200

class ManagerApprovalApi(Resource):
    @auth_required('token', 'session')  
    def post(self):
        user_id = current_user.id
        data = ManagerApproval(user_id = user_id )
        db.session.add(data)
        db.session.commit()
        return "Manager Approval added successfully", 200
    
    @auth_required('token', 'session')
    def get(self):
        user_ids = ManagerApproval.query.all()
        result = []
        for user_id in user_ids:
            user = User.query.get(user_id.user_id)
            result.append({
                'user_id': user_id.user_id,
                'id': user_id.id,
                'user_name':user.username
            })
        return result, 200
    
    @auth_required('token', 'session')
    @roles_required('admin')
    def delete(self):
        id = request.args.get('id')
        if id:
            row = ManagerApproval.query.get(id)
            if row:
                db.session.delete(row)
                db.session.commit()
                return "row deleted successfully", 200
            else:
                return "entry not found", 404
        else:
            return "No user id provided", 400
    
