from flask import Blueprint
auth_blueprint = Blueprint('auth', __name__)
df_auth_blueprint = Blueprint('df_auth', __name__)


@auth_blueprint.before_request
def before_request():
	pass


@auth_blueprint.after_request
def after_request(response):
	return response


# from flask_httpauth import HTTPTokenAuth
# token_auth = HTTPTokenAuth()

# @token_auth.verify_token
# def verify_token(token=None):
# 	return True

from flask_restful import Api
api = Api(auth_blueprint)

from .merchant_login_api import (MerchantLoginAPI,MerchantPassportAPI)
api.add_resource(MerchantLoginAPI, '/merchant/login')
api.add_resource(MerchantPassportAPI, '/merchant/passport')

from .admin_login_api import (AdminLoginAPI,AdminPassportAPI)
api.add_resource(AdminLoginAPI, '/admin/login')
api.add_resource(AdminPassportAPI, '/admin/passport')

df_api = Api(df_auth_blueprint)
df_api.add_resource(MerchantLoginAPI, '/merchant/login')
df_api.add_resource(MerchantPassportAPI, '/merchant/passport')
df_api.add_resource(AdminLoginAPI, '/admin/login')
df_api.add_resource(AdminPassportAPI, '/admin/passport')


