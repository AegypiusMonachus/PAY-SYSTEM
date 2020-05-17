from flask import Blueprint
from app.auth.common import token_auth

api_0_1_df_blueprint = Blueprint('api_0_1_df', __name__)

@api_0_1_df_blueprint.before_request
@token_auth.login_required
def before_request():
    pass


@api_0_1_df_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(api_0_1_df_blueprint)


# 代付商户路由
from app.api_0_1.resources.df_merchant_api import Df_merchant,Aboutagent
api.add_resource(Df_merchant, '/df/merchant')
api.add_resource(Aboutagent, '/df/aboutagent/<string:mer_code>')

# 代付商户路由
from app.api_0_1.resources.df_agent_api import Df_agent
api.add_resource(Df_agent, '/df/agent')

# from app.api_0_1.resources.df_credit_api import DfCredit
# api.add_resource(DfCredit, '/df/credit')

from app.api_0_1.resources.df_wraw_api import DfWrawApi,DfWrawTotalApi
api.add_resource(DfWrawApi, '/df/wraw','/df/wraw/<string:order_no>')
api.add_resource(DfWrawTotalApi, '/df/wrawtotal')

#充值查询
from app.api_0_1.resources.df_credit_api import DfCredit
api.add_resource(DfCredit, '/df/recharge')



from app.api_0_1.resources.df_agents_resports_api import DfAgentsResportsApi
api.add_resource(DfAgentsResportsApi, '/df/agents/resports')

# 充值报表查询
from app.api_0_1.resources.df_mer_recharge_baobiao_api import Dfmer_chongzhi
api.add_resource(Dfmer_chongzhi, '/df/recharge/report')

from app.api_0_1.resources.bank_api import (
    Bank,
    MerBank
)
api.add_resource(Bank, '/bank')
api.add_resource(MerBank, '/merbank')

from app.api_0_1.resources.qrcode_api import  Get_level
api.add_resource(Get_level, '/getlevel')




