import datetime
import time

from flask import g
from flask_restful import Resource
from sqlalchemy import func

from app.api_0_1.common import make_response
from app.common import keep_two_del
from app.models import db
from app.models.df_trade_dao import DfTradeRechargeDao, DfTradeDao
from app.models.merchant_dao import MerchantDao
from app.service.df_mer_statistics_service import tongji, ag_tongji


class Df_mer_tongji(Resource):
    def get(self):
        critern = set()
        zeroPoint = int(time.time()) - int(time.time() - time.timezone) % 86400
        shijiancuo = int(time.time())
        if g.current_member:
            username = g.current_member.username
            critern.add(DfTradeDao.mer_username == username)
            critern.add(DfTradeDao.state == 2)
            critern.add(zeroPoint <= DfTradeDao.action_time)
            critern.add(DfTradeDao.action_time <= shijiancuo)


        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        res = tongji(critern)
        times = res[0][0]
        real_amount_sum = res[0][1]
        result = []

        data = {}
        data['number_day'] = times
        data["sum_amount_day"] = float('%.2f' % keep_two_del(real_amount_sum))

        # 今天日期
        today = datetime.date.today()
        # 昨天时间
        yesterday = today - datetime.timedelta(days=1)
        # 昨天开始时间戳
        yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
        # 昨天完成时间戳
        yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
        args = db.session.query(
            func.coalesce(func.count(DfTradeDao.mer_username == g.current_member.username), 0).label('times'),
            func.coalesce(func.sum(DfTradeDao.amount), 0).label('real_amount_sum')).filter(yesterday_start_time <= DfTradeDao.action_time,
                                                                                            DfTradeDao.mer_username == username,DfTradeDao.state == 2,
                                                                                            DfTradeDao.action_time <= yesterday_end_time).all()
        ytimes = args[0][0]
        yreal_amount_sum = args[0][1]
        data['number_yes'] = ytimes
        data["sum_amount_yes"] = float('%.2f' % keep_two_del(yreal_amount_sum))
        result.append(data)
        return make_response(result)



class Df_agent_tongji(Resource):
    def get(self):
        username = g.current_member.username
        if not username:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }

        res = ag_tongji()
        return make_response(res)