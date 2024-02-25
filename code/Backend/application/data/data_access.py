from application.data.models import Product, Category
from flask import current_app as app
from flask_caching import Cache

cache = Cache(app)
app.app_context().push()

@cache.memoize(60)
def get_all_products():
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
    return result
