from flask import Blueprint
from app.auth.common import token_auth


api_0_1_blueprint = Blueprint('api_0_1', __name__)
df_api_0_1_blueprint = Blueprint('df_api_0_1', __name__)

@api_0_1_blueprint.before_request
@token_auth.login_required
def before_request():
    pass


@api_0_1_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(api_0_1_blueprint)
df_api = Api(df_api_0_1_blueprint)

from .resources.merchants_api import MerchantAPI
api.add_resource(MerchantAPI, '/merchant', '/merchant/<int:id>')

from .resources.agent_api import Agents
api.add_resource(Agents, '/agents', '/agents/<string:code>')


from .resources.agents_resports_api import (AgentsResports,AgentsResportsTotal)
api.add_resource(AgentsResports, '/agents/resports')
api.add_resource(AgentsResportsTotal, '/agents/resports/total')

from .resources.onlinetrades_api import (onlinetradesAPI,OnlinetradesTotalAPI)
api.add_resource(onlinetradesAPI, '/onlinetrades')
api.add_resource(OnlinetradesTotalAPI, '/onlinetrades/total')


from .resources.withdraw_api import withdrawAPI, WithdrawTotalAPI
api.add_resource(withdrawAPI, '/withdraw')
api.add_resource(WithdrawTotalAPI, '/withdrawtotal')
df_api.add_resource(withdrawAPI, '/withdraw')
df_api.add_resource(WithdrawTotalAPI, '/withdrawtotal')

from .resources.getsend_api import GetSend
api.add_resource(GetSend, '/getsend')

from .resources.agent_api import getNumMerchar
api.add_resource(getNumMerchar, '/getnummerchar')

from .resources.banktrades_api import BanktradesAPI
api.add_resource(BanktradesAPI, '/banktrades','/banktrades/<int:id>')
from .resources.refulation_api import refulationApi
api.add_resource(refulationApi, '/refulation')


from .resources.refulation_api import GetDefaultAgents
api.add_resource(GetDefaultAgents, '/getdefaultagents')

from .resources.bank_api import (
	Bank,
	MerBank
)
api.add_resource(Bank, '/bank')
api.add_resource(MerBank, '/merbank')

from .resources.qrcode_api import QrcodeApi, Get_level, Get_bank_name, Tupian, CancelQrcode
api.add_resource(QrcodeApi, '/qrcode')
api.add_resource(Get_level, '/getlevel')
api.add_resource(Get_bank_name, '/getbankname')
api.add_resource(Tupian, '/tupian')
api.add_resource(CancelQrcode, '/cancelqrcode')


from .resources.manual_match_api import ManualMatchApi,ManualMatchDetailApi
api.add_resource(ManualMatchApi, '/manual')
api.add_resource(ManualMatchDetailApi, '/manual_detail')


from .resources.statistical_api import StatisticalApi, StatisticalKkApi
api.add_resource(StatisticalApi, '/statistical')
api.add_resource(StatisticalKkApi, '/statistical_kk')


from app.api_0_1.resources.resports_api import Resports
api.add_resource(Resports, '/get/resports')


from app.api_0_1.resources.qrcode_api import Signs, SignsQRcode, EditQRcode, GetQRcodeSign
api.add_resource(Signs, '/signs')
api.add_resource(SignsQRcode, '/signs/qrcode')
api.add_resource(EditQRcode, '/edit/qrcode')
api.add_resource(GetQRcodeSign, '/get/signs/qrcode')

from app.api_0_1.trades_bank import TradesBankAPI
api.add_resource(TradesBankAPI, '/trades/bank')

from app.api_0_1.trades_cancel_confirmed_finished import TradesCancelConfirmed , TradesConfirmedFinished, TradesConfirmedCancel
api.add_resource(TradesCancelConfirmed, '/cancel/confirmed')
api.add_resource(TradesConfirmedFinished, '/confirmed/finished')
api.add_resource(TradesConfirmedCancel, '/confirmed/cancel')

from app.api_0_1.entries import OrderEntryAPI, MerchantEntryAPI
api.add_resource(OrderEntryAPI, '/order/entry')
api.add_resource(MerchantEntryAPI, '/merchant/entry')
from app.api_0_1.trades_created_finished import TradesCreatedFinished
api.add_resource(TradesCreatedFinished, '/created/finished')
from app.api_0_1.resources.name_like_search import NameLikeSearch
api.add_resource(NameLikeSearch, '/likesearch')

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
api.add_resource(DfWrawApi, '/df/wraw')
api.add_resource(DfWrawTotalApi, '/df/wrawtotal')

#充值查询
from app.api_0_1.resources.df_credit_api import DfCredit
api.add_resource(DfCredit, '/df/recharge')



from app.api_0_1.resources.df_agents_resports_api import DfAgentsResportsApi
api.add_resource(DfAgentsResportsApi, '/df/agents/resports')

# 充值报表查询
from app.api_0_1.resources.df_mer_recharge_baobiao_api import Dfmer_chongzhi
api.add_resource(Dfmer_chongzhi, '/df/recharge/report')
