from flask_restful import Resource
from app.service.agents_resports_service import AgentsResportsService
from app.api_0_1.common import make_response
from app.api_0_1.parsers.agents_resports_parser import agentsparserresports
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.merchant_dao import MerchantDao
from app.models.withdraw_dao import WithdrawDao
from flask import g
from app.api_0_1.utils import SECONDS_PER_DAY
from app.models import db
from sqlalchemy import func
from app.common import keep_two_del
import time
from datetime import datetime, timedelta, date
from decimal import *


def tupinlist(fn):
    res_list = []
    for i in fn:
        i = list(i)
        res_list.append(i)
    return res_list


class AgentsResports(Resource):
    def get(self):
        m_args = agentsparserresports.parse_args(strict=True)
        critern = set()
        critern_name = set()
        critern_wraw = set()
        critern_name.add(MerchantDao.type == 1)

        if g.current_member:
            username = g.current_member.username
            critern_name.add(MerchantDao.parent_name == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }

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
        q = res.get_data_agents_resports(args = critern,page = m_args['page'],per_page = m_args['page_size'],critern_name = critern_name,critern_wraw=critern_wraw)

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
        # m_args = agentsparserresportstotal.parse_args(strict=True)

        if g.current_member:
            username = g.current_member.username
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }

        res_mer = db.session.query(MerchantDao).filter(MerchantDao.username==username).first()
        if res_mer.type == 2:

            now = date.today()
            yesterday = now - timedelta(days=1)
            tom = now + timedelta(days=1)
            now_time = int(time.mktime(now.timetuple()))
            yesterday_time = int(time.mktime(yesterday.timetuple()))
            tom_time = int(time.mktime(tom.timetuple()))

            res_merchant_list = db.session.query(MerchantDao).filter(MerchantDao.parent_name == username).all()
            res_list = []
            for i in res_merchant_list:
                res_list.append(i.code)

            res_total = db.session.query(
                OnlinetradesDao.mer_code,
                OnlinetradesDao.user_name,
                func.sum(OnlinetradesDao.bank_amount).label('amount'),
                func.sum(OnlinetradesDao.real_cost_agent).label('real_cost_agent')
            ).filter(OnlinetradesDao.state == 2, OnlinetradesDao.audit_time.between(yesterday_time, now_time)).group_by(OnlinetradesDao.mer_code,
                                                                    OnlinetradesDao.user_name).all()

            res_total_list = []
            for i in res_total:
                if i.mer_code in res_list:
                    res_total_list.append(i)
            res_total_list_1 = tupinlist(res_total_list)

            res_total_n = db.session.query(
                OnlinetradesDao.mer_code,
                OnlinetradesDao.user_name,
                func.sum(OnlinetradesDao.bank_amount).label('amount'),
                func.sum(OnlinetradesDao.real_cost_agent).label('real_cost_agent')
            ).filter(OnlinetradesDao.state == 2, OnlinetradesDao.audit_time.between(now_time, tom_time)).group_by(
                OnlinetradesDao.mer_code,
                OnlinetradesDao.user_name).all()

            res_total_list_n = []
            for i in res_total_n:
                if i.mer_code in res_list:
                    res_total_list_n.append(i)
            res_total_list_2 = tupinlist(res_total_list_n)


            data_list = [Decimal(0), Decimal(0), Decimal(0), Decimal(0)]
            for i in res_total_list_1:
                data_list[0] += i[2]
                data_list[1] += i[3]

            for i in res_total_list_2:
                data_list[2] += i[2]
                data_list[3] += i[3]

            agent_amount = db.session.query(MerchantDao.amount).filter(MerchantDao.username == username).scalar()
            data_list.append(agent_amount)

            result = []
            result.append({
                "y_total_amount": float(keep_two_del(data_list[0])),  # 昨日交易金额
                "y_cost_agent": float(keep_two_del(data_list[1])),  # 昨日代理费
                "n_total_amount": float(keep_two_del(data_list[2])),  # 今日交易金额
                "n_cost_agent": float(keep_two_del(data_list[3])),  # 今日代理费
                "amount": float(keep_two_del(data_list[4]))
            })
            return make_response(result)

        else:
            return {'success': False, 'errorMsg': "您不是代理"}
