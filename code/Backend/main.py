from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.data.models import User, Role
from application.data.database import db
from application.config import LocalDevelopmentConfig
from flask_cors import CORS
from flask_restful import Resource, Api
from application.utils import helpers
from application.jobs import workers

app = None
api = None
celery = None

app = Flask(__name__)
CORS(app)

#connect to the database
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
app.app_context().push()

#Setting up flask Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

# setting up api
api = Api(app)
app.app_context().push()

# setting up celery
celery = workers.celery

#Update with configuration

celery.conf.update(
    broker_url = app.config['CELERY_BROKER_URL'],
    backend_url = app.config['CELERY_BACKEND_URL']
)

celery.Task = workers.ContextTasK
app.app_context().push()

from application.controller.api import AssignRoleApi, registerApi, CategoryApi, ProductApi, \
    GetAllProduct, CartApi, CheckRoleApi, SearchApi, callCeleryApi, sendCsvApi, CategoryApproveApi, sendBarPlotPdf, buyAll, ManagerApprovalApi, getCachedProducts

api.add_resource(AssignRoleApi, '/api/role')
api.add_resource(registerApi, '/register1')
api.add_resource(CategoryApi, '/api/category')
api.add_resource(ProductApi, '/api/product')
api.add_resource(GetAllProduct, '/api/allproducts')
api.add_resource(CartApi, '/api/cart')
api.add_resource(CheckRoleApi, '/api/checkrole')
api.add_resource(SearchApi, '/api/search')
api.add_resource(callCeleryApi, '/api/celery')
api.add_resource(sendCsvApi, '/api/send_csv')
api.add_resource(CategoryApproveApi, '/api/category_approve')
api.add_resource(sendBarPlotPdf, '/api/send_bar_plot_pdf')  
api.add_resource(buyAll, '/api/buy_all')
api.add_resource(ManagerApprovalApi,'/api/manager_approval')
api.add_resource(getCachedProducts, '/api/get_cached_products')
if __name__ =='__main__':
    app.run(host = '0.0.0.0', port = 8000)