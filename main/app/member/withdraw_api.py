from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
from app.api_0_1.parsers.onlinetrades_parser import withdrawParsers,withdrawParserspost,withdrawParsersput,getsendParsers
from app.api_0_1.common import make_fields, make_response
from app.service.withdraw_service import getOnlineData,insert,getstate,update, getwithdraw_total
from app.models.withdraw_dao import WithdrawDao
from app.models.merchant_dao import MerchantBank,MerchantDao
from app.api_0_1.utils import SECONDS_PER_DAY
from flask import g
from app.common import keep_two_del
from app.models import db

class withdrawAPI(Resource):
    def get(self):
        m_args = withdrawParsers.parse_args(strict=True)
        critern = set()
        if 'mer_code' in m_args:
            if m_args['mer_code'] is not None:
                critern.add(MerchantDao.username == m_args['mer_code'])
        if g.current_member:
            username = g.current_member.username
            print(username)
            type = g.current_member.type
            critern.add(WithdrawDao.mer_name == username)
            critern.add(MerchantDao.type == type)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        if 'bank_id' in m_args:
            if m_args['bank_id'] is not None:
                critern.add(MerchantBank.bankNumber == m_args['bank_id'])
        if 'bank_account' in m_args:
            if m_args['bank_account'] is not None:
                critern.add(MerchantDao.parent_code == m_args['bank_account'])
        if 'order_no' in m_args:
            if m_args['order_no'] is not None:
                critern.add(WithdrawDao.order_no == m_args['order_no'])
        if 'amount_max' in m_args:
            if m_args['amount_max'] is not None:
                critern.add(WithdrawDao.amount <= m_args['amount_max'])
        if 'amount_min' in m_args:
            if m_args['amount_min'] is not None:
                critern.add(WithdrawDao.amount >= m_args['amount_min'])
        if 'state' in m_args:
            if m_args['state'] is not None:
                critern.add(WithdrawDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern.add(WithdrawDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(WithdrawDao.action_time <= m_args['end_time'])
        if m_args['begin_time_au'] is not None:
            critern.add(WithdrawDao.audit_time >= m_args['begin_time_au'])
        if m_args['end_time_au'] is not None:
            critern.add(WithdrawDao.audit_time <= m_args['end_time_au'])
        if m_args['account'] is not None:
            critern.add(WithdrawDao.account == m_args['account'])

        res = getOnlineData(critern, page=m_args['page'], per_page=m_args['page_size'])
        result = []
        for items in res.items:
            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0
            if items.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(items.wrdraw_amount))
            else:
                wrdraw_amount = 0

            if items.paid_amount is not None:
                paid_amount = float('%.2f' % keep_two_del(items.paid_amount))
            else:
                paid_amount = 0
            if items.real_amount is not None:
                real_amount = float('%.2f' % keep_two_del(items.real_amount))
            else:
                real_amount = 0

            if items.cost_sx is not None:
                cost_sx = float('%.2f' % keep_two_del(items.cost_sx))
            else:
                cost_sx = 0

            result.append({
                "mer_code": items.mer_code,
                "username": items.username,
                "order_no": items.order_no,
                "bank_id": items.bank_id,
                "bank_name": items.bank_name,
                "amount": amount,
                "wrdraw_amount": wrdraw_amount,
                "paid_amount": paid_amount,
                "account": items.account,
                "name": items.name,
                "real_amount": real_amount,
                "action_time": items.action_time,
                "audit_time": items.audit_time,
                "cost_sx": cost_sx,
                "state": items.state,
                "remark": items.remark,
                "audit_name": items.audit_name,
                "mer_ip": items.mer_ip
            })
        return make_response(result, page=res.page, pages=res.pages, total=res.total)


    def post(self):
        m_args = withdrawParserspost.parse_args(strict=True)
        res = insert(m_args)
        if res is not None:
            if res['errorCode'] == 403:
                return {
                    'success': False,
                    'errorCode': 403,
                    'errorMsg': '该用户不存在'
                }
            if res['errorCode'] == 404:
                return {
                    'success': False,
                    'errorCode': 404,
                    'errorMsg': '余额不足'
                }
        return {'success': True}


    # def put(self):
    #     m_args = withdrawParsersput.parse_args(strict=True)
    #     res = getstate(m_args['order_no'])
    #     if res is None:
    #         return {
    #             'success': False,
    #             'errorCode': 403,
    #             'errorMsg': '该订单不存在'
    #         }
    #     if m_args['state'] == 1:
    #         return {
    #             'success': False,
    #             'errorCode': 403,
    #             'errorMsg': '该订单状态错误'
    #         }
    #     states = res.state
    #     if states != 1:
    #         return {
    #             'success': False,
    #             'errorCode': 403,
    #             'errorMsg': '该订单状态错误，请确认订单是否完成或者取消'
    #         }
    #     else:
    #         if m_args['state'] == 2:
    #             up = update(m_args)
    #         if m_args['state'] == 3:
    #             up = update(m_args)
    #         if up is None:
    #             return {
    #                 'success': True,
    #                 'errorCode': 400,
    #                 'errorMsg': '入款成功'
    #             }
    #         else:
    #             if up['errorCode'] == 403:
    #                 return {
    #                     'success': False,
    #                     'errorCode': 403,
    #                     'errorMsg': '该用户不存在'
    #                 }
    #             if up['errorCode'] == 404:
    #                 return {
    #                     'success': False,
    #                     'errorCode': 403,
    #                     'errorMsg': '取款金额不能大于用户余额'
    #                 }



class WithdrawTotalAPI(Resource):
    def get(self):
        m_args = withdrawParsers.parse_args(strict=True)

        critern = set()
        if 'mer_code' in m_args:
            if m_args['mer_code'] is not None:
                critern.add(MerchantDao.username == m_args['mer_code'])
        if g.current_member:
            username = g.current_member.username
            type = g.current_member.type
            critern.add(WithdrawDao.mer_name == username)
            critern.add(MerchantDao.type == type)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        if 'bank_id' in m_args:
            if m_args['bank_id'] is not None:
                critern.add(MerchantBank.bankNumber == m_args['bank_id'])
        if 'bank_account' in m_args:
            if m_args['bank_account'] is not None:
                critern.add(MerchantDao.parent_code == m_args['bank_account'])
        if 'order_no' in m_args:
            if m_args['order_no'] is not None:
                critern.add(WithdrawDao.order_no == m_args['order_no'])
        if 'amount_max' in m_args:
            if m_args['amount_max'] is not None:
                critern.add(WithdrawDao.amount <= m_args['amount_max'])
        if 'amount_min' in m_args:
            if m_args['amount_min'] is not None:
                critern.add(WithdrawDao.amount >= m_args['amount_min'])
        if 'state' in m_args:
            if m_args['state'] is not None:
                critern.add(WithdrawDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern.add(WithdrawDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(WithdrawDao.action_time <= m_args['end_time'])
        if m_args['begin_time_au'] is not None:
            critern.add(WithdrawDao.audit_time >= m_args['begin_time_au'])
        if m_args['end_time_au'] is not None:
            critern.add(WithdrawDao.audit_time <= m_args['end_time_au'])

        res = getwithdraw_total(critern)

        result = []
        for items in res:
            if items.amount_sum is not None:
                amount_sum = float('%.2f' % keep_two_del(items.amount_sum))
            else:
                amount_sum = 0
            if items.paid_amount is not None:
                paid_amount = float('%.2f' % keep_two_del(items.paid_amount))
            else:
                paid_amount = 0
            if items.withdraw_amount_sum is not None:
                withdraw_amount_sum = float('%.2f' % keep_two_del(items.withdraw_amount_sum))
            else:
                withdraw_amount_sum = 0

            result.append({
                "amount_sum": amount_sum,
                "paid_amount_sum": paid_amount,
                "withdraw_amount_sum": withdraw_amount_sum
            })

        return make_response(result)



class GetTranslate(Resource):
    def get(self):
        critern = set()
        if g.current_member:
            username = g.current_member.username
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        res = db.session.query(
            (MerchantDao.amount - MerchantDao.wrdraw_amount).label('kyamount')
        ).filter(MerchantDao.username == username).first()
        if res is not None:
            if res.kyamount is not None:
                res = float('%.2f' % keep_two_del(res.kyamount))
            else:
                res = 0
        else:
            res = 0

        return {'kyamount':res}




