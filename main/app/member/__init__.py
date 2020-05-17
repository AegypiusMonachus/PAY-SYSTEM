from flask import Blueprint
from app.auth.common import token_auth

member_blueprint = Blueprint('member', __name__)
df_member_blueprint = Blueprint('df_member', __name__)


@member_blueprint.before_request
@df_member_blueprint.before_request
@token_auth.login_required
def before_request():
    pass


@member_blueprint.after_request
@df_member_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(member_blueprint)
df_api = Api(df_member_blueprint)

from app.member.merchants_api import MerchantAPI, MerchantInfoAPI, Changepassworld
api.add_resource(MerchantAPI, '/merchant', '/merchant/<int:id>')
api.add_resource(MerchantInfoAPI, '/merchantinfo')
api.add_resource(Changepassworld, '/changepd')
df_api.add_resource(MerchantInfoAPI, '/merchantinfo')



from app.member.agent_api import Agents
api.add_resource(Agents, '/agents', '/agents/<string:code>')

from app.member.onlinetrades_api import (onlinetradesAPI,OnlinetradesTotalAPI)
api.add_resource(onlinetradesAPI, '/onlinetrades')
api.add_resource(OnlinetradesTotalAPI, '/onlinetrades/total')
df_api.add_resource(onlinetradesAPI, '/onlinetrades')
df_api.add_resource(OnlinetradesTotalAPI, '/onlinetrades/total')

from app.member.onlinetrades_api import GetOnlinetradesDatilAPI
api.add_resource(GetOnlinetradesDatilAPI, '/onlinetrades/datilsum')


from app.member.withdraw_api import withdrawAPI, WithdrawTotalAPI,GetTranslate
api.add_resource(withdrawAPI, '/withdraw')
api.add_resource(WithdrawTotalAPI, '/withdrawtotal')
api.add_resource(GetTranslate, '/getranslate')
df_api.add_resource(withdrawAPI, '/withdraw')
df_api.add_resource(WithdrawTotalAPI, '/withdrawtotal')
df_api.add_resource(GetTranslate, '/getranslate')


from app.member.agent_api import getNumMerchar
api.add_resource(getNumMerchar, '/getnummerchar')

from app.member.banktrades_api import BanktradesAPI
api.add_resource(BanktradesAPI, '/banktrades','/banktrades/<int:id>')
from app.member.refulation_api import refulationApi
api.add_resource(refulationApi, '/refulation')

from app.member.bank_api import (
	Bank,
	MerBank
)
api.add_resource(Bank, '/bank')
api.add_resource(MerBank, '/merbank')
df_api.add_resource(Bank, '/bank')
df_api.add_resource(MerBank, '/merbank')

from app.member.qrcode_api import QrcodeApi, Get_level, Get_bank_name
api.add_resource(QrcodeApi, '/qrcode')
api.add_resource(Get_level, '/getlevel')
api.add_resource(Get_bank_name, '/getbankname')


from app.member.agents_resports_mem_api import (AgentsResports,AgentsResportsTotal)
api.add_resource(AgentsResports, '/agents/resports')
api.add_resource(AgentsResportsTotal, '/agents/resports/total')

from app.member.agent_statistical_api import AgentStatisticalApi
api.add_resource(AgentStatisticalApi, '/agentstatistical')

from app.member.df_bank_api import DfBank
api.add_resource(DfBank, '/dfbank')
df_api.add_resource(DfBank, '/dfbank')

from app.member.df_credit_api import DfCredit
# api.add_resource(DfCredit, '/df/recharge')
df_api.add_resource(DfCredit, '/df/recharge')


from app.member.df_payment_result import PaymentResult
api.add_resource(PaymentResult, '/payment/result')


from app.member.df_wraw_api import DfWrawApi,DfWrawTotalApi
# api.add_resource(DfWrawApi, '/df/wraw')
# api.add_resource(DfWrawTotalApi, '/df/wrawtotal')
df_api.add_resource(DfWrawApi, '/df/wraw')
df_api.add_resource(DfWrawTotalApi, '/df/wrawtotal')

from app.member.df_merchant_api import Get_merinfo,Get_aginfo,Get_agrateinfo
# api.add_resource(Get_merinfo, '/dfmerinfo')
# api.add_resource(Get_aginfo, '/df/agent/merinfo')
# api.add_resource(Get_agrateinfo, '/df/agent/rateinfo')
df_api.add_resource(Get_merinfo, '/dfmerinfo')
df_api.add_resource(Get_aginfo, '/df/agent/merinfo')
df_api.add_resource(Get_agrateinfo, '/df/agent/rateinfo')



# 代付商户和代付代理的统计
from app.member.df_merchant_statistics_api import Df_mer_tongji,Df_agent_tongji
# api.add_resource(Df_mer_tongji, '/df/tongji')
# api.add_resource(Df_agent_tongji, '/df/agent/tongji')

df_api.add_resource(Df_mer_tongji, '/df/tongji')
df_api.add_resource(Df_agent_tongji, '/df/agent/tongji')

from app.member.df_agents_resports_api import DfAgentsResportsApi
# api.add_resource(DfAgentsResportsApi, '/df/agents/resports')
df_api.add_resource(DfAgentsResportsApi, '/df/agents/resports')

#代付商户充值
from app.member.df_merchant_recharge_api import (DfRechargeBankAPI,DfMerchantRechargeAPI)
df_api.add_resource(DfRechargeBankAPI, '/df/recharge/bank')
df_api.add_resource(DfMerchantRechargeAPI, '/recharge')

