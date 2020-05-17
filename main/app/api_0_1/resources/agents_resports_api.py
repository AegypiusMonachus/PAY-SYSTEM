from flask_restful import Resource
from app.service.agents_resports_service import AgentsResportsService
from ..common import make_response
from app.api_0_1.parsers.agents_resports_parser import agentsparserresportsguanli,agentsparserresportstotalguanli
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.merchant_dao import MerchantDao
from app.models.withdraw_dao import WithdrawDao
from app.common import keep_two_del

class AgentsResports(Resource):
    def get(self,mercode=None):
        m_args = agentsparserresportsguanli.parse_args(strict=True)
        critern = set()
        critern_wraw = set()
        critern_name = set()
        critern_name.add(MerchantDao.type == 1)

        if m_args['mer_username'] is not None:
            critern_name.add(MerchantDao.parent_name == m_args['mer_username'])
        if m_args['begin_time'] is not None:
            critern.add(OnlinetradesDao.action_time >= m_args['begin_time'])
            critern_wraw.add(WithdrawDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(OnlinetradesDao.action_time <= m_args['end_time'])
            critern_wraw.add(WithdrawDao.action_time >= m_args['end_time'])
        if m_args['state'] is not None:
            critern.add(OnlinetradesDao.state == m_args['state'])
            critern_wraw.add(WithdrawDao.action_time >= m_args['state'])

        res  = AgentsResportsService()
        if mercode is None:
            q = res.get_data_agents_resports(args = critern,page = m_args['page'],per_page = m_args['page_size'],critern_name = critern_name,critern_wraw = critern_wraw)
        else:
            critern.add(MerchantDao.parent_name == m_args['state'])
            q = res.get_data_agents_resports_merchat(critern, m_args['page'], m_args['page_size'])
        result = []
        for i in q.items:
            if i.cost_agent is not None:
                cost_agent = float('%.2f' % keep_two_del(i.cost_agent))
            else:
                cost_agent = 0
            if i.cost_agent_completed is not None:
                cost_agent_completed = float('%.2f' % keep_two_del(i.cost_agent_completed))
            else:
                cost_agent_completed = 0
            if i.cost_agent_hang is not None:
                cost_agent_hang = float('%.2f' % keep_two_del(i.cost_agent_hang))
            else:
                cost_agent_hang = 0

            if i.wrdraw_amount_completed is not None:
                wrdraw_amount_completed = float('%.2f' % keep_two_del(i.wrdraw_amount_completed))
            else:
                wrdraw_amount_completed = 0
            if i.wrdraw_amount_hang is not None:
                wrdraw_amount_hang = float('%.2f' % keep_two_del(i.wrdraw_amount_hang))
            else:
                wrdraw_amount_hang = 0
            if i.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(i.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                'parent_name': i.parent_name,
                'cost_agent': cost_agent,
                'cost_agent_completed': cost_agent_completed,
                'cost_agent_hang': cost_agent_hang,
                'wrdraw_amount_completed': wrdraw_amount_completed,
                'wrdraw_amount_hang': wrdraw_amount_hang,
                'wrdraw_amount': wrdraw_amount,
            })
        return make_response(result, page=q.page, pages=q.pages, total=q.total)


class AgentsResportsTotal(Resource):
    def get(self):
        m_args = agentsparserresportstotalguanli.parse_args(strict=True)
        del m_args['page']
        del m_args['page_size']
        critern = set()
        critern_name = set()
        critern_wraw = set()
        critern_name.add(MerchantDao.type == 1)
        if m_args['mer_username'] is not None:
            critern_name.add(MerchantDao.parent_name == m_args['mer_username'])
        if m_args['begin_time'] is not None:
            critern.add(OnlinetradesDao.action_time >= m_args['begin_time'])
            critern_wraw.add(WithdrawDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(OnlinetradesDao.action_time <= m_args['end_time'])
            critern_wraw.add(WithdrawDao.action_time >= m_args['end_time'])
        if m_args['state'] is not None:
            critern.add(OnlinetradesDao.state == m_args['state'])
            critern_wraw.add(WithdrawDao.action_time >= m_args['state'])

        res = AgentsResportsService()
        q = res.get_data_agents_resports_total(args=critern,critern_name=critern_name,critern_wraw=critern_wraw)

        result = []
        for i in q:
            if i.cost_agent_total is not None:
                cost_agent_total = float('%.2f' % keep_two_del(i.cost_agent_total))
            else:
                cost_agent_total = 0
            if i.cost_agent_completed_total is not None:
                cost_agent_completed_total = float('%.2f' % keep_two_del(i.cost_agent_completed_total))
            else:
                cost_agent_completed_total = 0
            if i.cost_agent_hang_total is not None:
                cost_agent_hang_total = float('%.2f' % keep_two_del(i.cost_agent_hang_total))
            else:
                cost_agent_hang_total = 0

            if i.wrdraw_amount_completed is not None:
                wrdraw_amount_completed = float('%.2f' % keep_two_del(i.wrdraw_amount_completed))
            else:
                wrdraw_amount_completed = 0
            if i.wrdraw_amount_hang is not None:
                wrdraw_amount_hang = float('%.2f' % keep_two_del(i.wrdraw_amount_hang))
            else:
                wrdraw_amount_hang = 0
            if i.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(i.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                'cost_agent_total': cost_agent_total,
                'cost_agent_completed_total': cost_agent_completed_total,
                'cost_agent_hang_total': cost_agent_hang_total,
                'wrdraw_amount_completed': wrdraw_amount_completed,
                'wrdraw_amount_hang': wrdraw_amount_hang,
                'wrdraw_amount': wrdraw_amount,
            })
        return make_response(result)