from flask import request
from flask_restful import Resource

from app.api_0_1.common import make_response
from app.api_0_1.parsers.df_merchant_parsers import df_merchant_recharge
from app.models.df_trade_dao import DfTradeRechargeDao
from app.service.dfmer_recharge_baobiao_service import test


class Dfmer_chongzhi(Resource):
    def get(self):
        args = df_merchant_recharge.parse_args()
        critern = set()
        critern.add(DfTradeRechargeDao.state == 2)

        if 'mer_name' in args:
            if args['mer_name'] is not None:
                critern.add(DfTradeRechargeDao.username == args['mer_name'])

        if 'begin_time' in args:
            if args['begin_time'] is not None:
                critern.add(DfTradeRechargeDao.action_time >= args['begin_time'])

        if 'end_time' in args:
            if args['end_time'] is not None:
                critern.add(DfTradeRechargeDao.action_time <= args['end_time'])

        pagination = test(critern, page=args['page'], per_page=args['page_size'])
        result=[]

        for item in pagination.items:
            result.append({
                "mer_name":item.username,
                "number_day":item.dds,
                "sum_amount_day":float('%.2f' % item.zje)
            })

        return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)



