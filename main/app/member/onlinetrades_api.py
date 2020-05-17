from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
from app.api_0_1.parsers.onlinetrades_parser import onlinetradesParsers
from app.api_0_1.common import make_fields, make_response
from app.service.onlinetrades_service import getOnlineData
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.merchant_dao import MerchantBank,MerchantDao,PayType
from app.api_0_1.utils import SECONDS_PER_DAY
from app.service.onlinetrades_service import get_online_data_datil,get_online_data_datil_yes,get_online_data_datil_day,get_online_data_datil_amount,get_online_data_datil_amount_number,getonline_total_mem
from flask import g
from app.common import keep_two_del

class onlinetradesAPI(Resource):
    def get(self):
        m_args = onlinetradesParsers.parse_args(strict=True)
        critern = set()
        if g.current_member:
            username = g.current_member.username
            critern.add(OnlinetradesDao.user_name == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        if m_args['mer_code'] is not None:
            critern.add(OnlinetradesDao.mer_code == m_args['mer_code'])
        if m_args['bank_id'] is not None:
            critern.add(MerchantBank.bankNumber == m_args['bank_id'])
        if m_args['agent_code'] is not None:
            critern.add(MerchantDao.parent_code == m_args['agent_code'])
        if m_args['org_order_no'] is not None:
            critern.add(OnlinetradesDao.org_order_no == m_args['org_order_no'])
        if m_args['amount_max'] is not None:
            critern.add(OnlinetradesDao.amount <= m_args['amount_max'])
        if m_args['amount_min'] is not None:
            critern.add(OnlinetradesDao.amount >= m_args['amount_min'])
        if m_args['state'] is not None:
            critern.add(OnlinetradesDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern.add(OnlinetradesDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(OnlinetradesDao.action_time <= m_args['end_time'])
        if m_args['begin_time_au'] is not None:
            critern.add(OnlinetradesDao.audit_time >= m_args['begin_time_au'])
        if m_args['end_time_au'] is not None:
            critern.add(OnlinetradesDao.audit_time <= m_args['end_time_au'])
        if m_args['pay_type_name'] is not None:
            critern.add(PayType.name == m_args['pay_type_name'])


        res = getOnlineData(critern,page=m_args['page'],per_page=m_args['page_size'])
        result = []
        for items in res.items:
            if items.real_cost_service is not None:
                real_cost_service = float('%.2f' % keep_two_del(items.real_cost_service))
            else:
                real_cost_service = 0
            if items.real_cost_agent is not None:
                real_cost_agent = float('%.2f' % keep_two_del(items.real_cost_agent))
            else:
                real_cost_agent = 0

            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0
            if items.real_amount is not None:
                real_amount = float('%.2f' % keep_two_del(items.real_amount))
            else:
                real_amount = 0

            if items.bank_amount is not None:
                bank_amount = float('%.2f' % keep_two_del(items.bank_amount))
            else:
                bank_amount = 0
            if items.cost_service is not None:
                cost_service = float('%.2f' % keep_two_del(items.cost_service))
            else:
                cost_service = 0

            if items.cost_agent is not None:
                cost_agent = float('%.2f' % keep_two_del(items.cost_agent))
            else:
                cost_agent = 0

            if items.cost_service_confirm is not None:
                cost_service_confirm = float('%.2f' % keep_two_del(items.cost_service_confirm))
            else:
                cost_service_confirm = 0

            if items.cost_agent_confirm is not None:
                cost_agent_confirm = float('%.2f' % keep_two_del(items.cost_agent_confirm))
            else:
                cost_agent_confirm = 0

            if items.amount_confirm is not None:
                amount_confirm = float('%.2f' % keep_two_del(items.amount_confirm))
            else:
                amount_confirm = 0

            if items.discount_amount is not None:
                discount_amount = float('%.2f' % keep_two_del(items.discount_amount))
            else:
                discount_amount = 0


            result.append({
                "order_no": items.order_no,
                "org_order_no": items.org_order_no,
                "bank_order_no": items.bank_order_no,
                "user_name": items.user_name,
                "qr_code": items.qr_code,
                "amount": amount,
                "real_amount": real_amount,
                "bank_amount": bank_amount,
                "discount_amount": discount_amount,
                "agents_name": items.agents_name,
                "action_time": items.action_time,
                "mer_code": items.mer_code,
                "pay_type": items.pay_type,
                "cost_service": cost_service,
                "cost_agent": cost_agent,
                "audit_time": items.audit_time,
                "state": items.state,
                "remark": items.remark,
                "bank_name": items.bank_name,
                "pay_type_name": items.pay_type_name,
                "amount_confirm": amount_confirm,
                "qr_code_confirm": items.qr_code_confirm,
                "audit_time_confirm": items.audit_time_confirm,
                "cost_service_confirm": cost_service_confirm,
                "cost_agent_confirm": cost_agent_confirm,
                "real_cost_service": real_cost_service,
                "real_cost_agent": real_cost_agent,
                "administrator_confirm": items.administrator_confirm,
                "mer_ip": items.mer_ip,
                "match_type":items.match_type
            })

        return make_response(result, page=res.page, pages=res.pages, total=res.total)


class GetOnlinetradesDatilAPI(Resource):
    def get(self):
        res = get_online_data_datil()
        res_amount = get_online_data_datil_amount()
        res_number = get_online_data_datil_amount_number()
        res_day = get_online_data_datil_day()
        res_yes = get_online_data_datil_yes()
        result = []
        args = {}
        if res is not None:
            args['sum_amount'] =float('%.2f' % keep_two_del(res.sum_amount))
        else:
            args['sum_amount'] =0
        if res_amount is not None:
            args['amount'] = float('%.2f' % keep_two_del(res_amount.amount))
        else:
            args['amount'] = 0
        if res_number is not None:
            args['number'] = int(res_number.number)
        else:
            args['number'] = 0
        if res_day is not None:
            args['sum_amount_day'] = float('%.2f' % keep_two_del(res_day.sum_amount_day))
        else:
            args['sum_amount_day'] = 0
        if res_yes is not None:
            args['sum_amount_yes'] = float('%.2f' % keep_two_del(res_yes.sum_amount_yes))
        else:
            args['sum_amount_yes'] = 0

        if res_day is not None:
            args['number_day'] = int(res_day.number_day)
        else:
            args['number_day'] = 0

        if res_yes is not None:
            args['number_yes'] = int(res_yes.number_yes)
        else:
            args['number_yes'] = 0
        result.append(args)
        return make_response(result)



class OnlinetradesTotalAPI(Resource):
    def get(self):
        m_args = onlinetradesParsers.parse_args(strict=True)
        critern = set()
        critern.add(PayType.code == 900001)
        if g.current_member:
            username = g.current_member.username
            critern.add(OnlinetradesDao.user_name == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }

        if m_args['mer_code'] is not None:
            critern.add(OnlinetradesDao.mer_code == m_args['mer_code'])
        if m_args['agent_code'] is not None:
            critern.add(MerchantDao.parent_code == m_args['agent_code'])
        if m_args['org_order_no'] is not None:
            critern.add(OnlinetradesDao.org_order_no == m_args['org_order_no'])
        if m_args['amount_max'] is not None:
            critern.add(OnlinetradesDao.amount <= m_args['amount_max'])
        if m_args['amount_min'] is not None:
            critern.add(OnlinetradesDao.amount >= m_args['amount_min'])
        if m_args['state'] is not None:
            critern.add(OnlinetradesDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern.add(OnlinetradesDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(OnlinetradesDao.action_time <= m_args['end_time'])
        if m_args['begin_time_au'] is not None:
            critern.add(OnlinetradesDao.audit_time >= m_args['begin_time_au'])
        if m_args['end_time_au'] is not None:
            critern.add(OnlinetradesDao.audit_time <= m_args['end_time_au'])
        if m_args['pay_type_name'] is not None:
            critern.add(PayType.name == m_args['pay_type_name'])
        res = getonline_total_mem(critern)


        result = []

        for items in res:
            if items.amount_sum is not None:
                amount_sum = float('%.2f' % keep_two_del(items.amount_sum))
            else:
                amount_sum = 0
            if items.real_amount_sum is not None:
                real_amount_sum = float('%.2f' % keep_two_del(items.real_amount_sum))
            else:
                real_amount_sum = 0

            if items.rcs_sum is not None:
                rcs_sum = float('%.2f' % keep_two_del(items.rcs_sum))
            else:
                rcs_sum = 0


            result.append({
                "amount_sum": amount_sum,
                "real_amount_sum": real_amount_sum,
                "rcs_sum": rcs_sum

            })



        return make_response(result)