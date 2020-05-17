from flask import Blueprint
from app.auth.common import token_auth

agentpay_blueprint = Blueprint('agentpay', __name__)


@agentpay_blueprint.before_request
# @token_auth.login_required
def before_request():
    pass


@agentpay_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(agentpay_blueprint)


from app.agentspay.df_test_api import TestApi
api.add_resource(TestApi,'/agentspay')

from app.agentspay.df_agentspay_api import AgentspayQueryApi
api.add_resource(AgentspayQueryApi,'/agentspay/query')


from app.agentspay.df_test_api import DownTestApi
api.add_resource(DownTestApi,'/downtest')

from app.agentspay.df_test_api import QueryTestApi
api.add_resource(QueryTestApi,'/querytest')

from app.agentspay.df_test_api import DFNotifyTestApi
api.add_resource(DFNotifyTestApi,'/dfnotifytest')

