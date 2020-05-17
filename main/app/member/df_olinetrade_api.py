from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
from app.api_0_1.parsers.onlinetrades_parser import onlinetradesParsers
from app.api_0_1.common import make_fields, make_response
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.merchant_dao import MerchantBank,MerchantDao,PayType
from app.api_0_1.utils import SECONDS_PER_DAY
from flask import g
from app.common import keep_two_del
from app.models.df_trade_dao import DfTradeDao
from app.service.df_olinetrade_service import getOnlineData
class DfWrawApi(Resource):
    def get(self):
        m_args = onlinetradesParsers.parse_args(strict=True)
        critern = set()
        if g.current_member:
            username = g.current_member.username
            critern.add(DfTradeDao.mer_username == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        # if m_args['username'] is not None:
        #     critern.add(DfTradeDao.mer_username == m_args['username'])
        if m_args['org_order_no'] is not None:
            critern.add(DfTradeDao.org_order_no == m_args['org_order_no'])
        if m_args['amount_max'] is not None:
            critern.add(DfTradeDao.amount <= m_args['amount_max'])
        if m_args['amount_min'] is not None:
            critern.add(DfTradeDao.amount >= m_args['amount_min'])
        if m_args['state'] is not None:
            critern.add(DfTradeDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern.add(DfTradeDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(DfTradeDao.action_time <= m_args['end_time'])
        if m_args['begin_time_au'] is not None:
            critern.add(DfTradeDao.audit_time >= m_args['begin_time_au'])
        if m_args['end_time_au'] is not None:
            critern.add(DfTradeDao.audit_time <= m_args['end_time_au'])


        res = getOnlineData(critern,page=m_args['page'],per_page=m_args['page_size'])
        result = []
        for items in res.items:


            if items.sxf is not None:
                sxf = float('%.2f' % keep_two_del(items.sxf))
            else:
                sxf = 0

            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0

            print(items.org_order_no,type(items.org_order_no))
            result.append({
                "id": items.id,
                "order_no": items.order_no,
                "org_order_no": items.org_order_no,
                "mer_code": items.mer_code,
                "mer_username": items.mer_username,
                "amount": amount,
                "action_time": items.action_time,
                "audit_time": items.audit_time,
                "state": items.state,
                "account_name": items.account_name,
                "account_no": items.account_no,
                "bank_name": items.bank_name,
                "sxf": sxf,
            })

        return make_response(result, page=res.page, pages=res.pages, total=res.total)