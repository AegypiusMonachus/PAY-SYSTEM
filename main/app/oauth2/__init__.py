from flask import Blueprint
oauth2_blueprint = Blueprint('oauth2', __name__)
df_oauth2_blueprint = Blueprint('df_oauth2', __name__)

@oauth2_blueprint.before_request
def before_request():
    pass


@oauth2_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(oauth2_blueprint)

from .merchant_auth_api import MerchantAuthAPI
api.add_resource(MerchantAuthAPI, '/merchant')

from .admin_auth_api import AdminAuthAPI
api.add_resource(AdminAuthAPI, '/admin')

df_api = Api(df_oauth2_blueprint)
df_api.add_resource(MerchantAuthAPI, '/merchant')
df_api.add_resource(AdminAuthAPI, '/admin')

