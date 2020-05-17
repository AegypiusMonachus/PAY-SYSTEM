from flask_restful import Resource
from app.service.df_agents_resports_service import DfAgentsResportsSer
from app.api_0_1.common import make_fields, make_response
from app.common import keep_two_del
from app.api_0_1.parsers.df_agents_resports_parsers import dfagentskkparser
from app.models.df_trade_dao import DfTradeSxfDao,DfTradeDao
from app.models.merchant_dao import MerchantDao
from flask import g
from app.models.df_agent_rate_dao import DfAgentRate

class DfAgentsResportsApi(Resource):
    def get(self):
        m_args = dfagentskkparser.parse_args(strict=True)
        critern = set()
        critern_name = set()
        critern_xinyong = set()
        critern_sxf = set()
        if g.current_member:
            if int(g.current_member.type) == 4:
                m_args['username'] = g.current_member.username
                critern.add(DfAgentRate.agent_name == m_args['username'])
            elif int(g.current_member.type) == 3:
                critern.add(DfAgentRate.mer_username == m_args['username'])
            else:
                return {"success": False, "errorCode": 8202 , "errorMsg": "该用户不是代理"}
        else:
            return {"success": False,"errorCode": 8202 , "errorMsg": "请登录"}
        if m_args['state'] is not None:
            critern_xinyong.add(DfTradeDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern_xinyong.add(DfTradeDao.action_time >= m_args['begin_time'])
            critern_sxf.add(DfTradeSxfDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern_xinyong.add(DfTradeDao.action_time <= m_args['end_time'])
            critern_sxf.add(DfTradeSxfDao.action_time <= m_args['end_time'])
        res_args = DfAgentsResportsSer().get_merchart(critern = critern,critern_xinyong = critern_xinyong,critern_sxf = critern_xinyong,page = m_args['page'], per_page = m_args['page_size'])
        result = []
        for res in res_args.items:
            if res.number is not None:
                number = int(res.number)
            else:
                number = 0

            if res.amount is not None:
                amount = float('%.2f' % keep_two_del(res.amount))
            else:
                amount = 0

            if res.sxf is not None:
                sxf = float('%.2f' % keep_two_del(res.sxf))
            else:
                sxf = 0
            result.append({
                'agent_name': res.agent_name,
                'number': number,
                'amount': amount,
                'sxf': sxf,
            })

        return make_response(result, page=res_args.page, pages=res_args.pages, total=res_args.total)

