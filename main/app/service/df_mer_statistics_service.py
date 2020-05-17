import datetime
import time

from flask import g
from sqlalchemy import func

from app.common import keep_two_del
from app.models import db
from app.models.df_agent_rate_dao import DfAgentRate
from app.models.df_trade_dao import DfTradeDao
from app.models.merchant_dao import MerchantDao


# 商户
def tongji(args):
    res = db.session.query(
        func.coalesce(func.count(DfTradeDao.mer_username == g.current_member.username), 0).label('times'),
        func.coalesce(func.sum(DfTradeDao.amount), 0).label('real_amount_sum')).filter(*args).all()

    return res

# 代理
def ag_tongji():

    result = []
    data = {}
    # 今日凌晨0点
    zeroPoint = int(time.time()) - int(time.time() - time.timezone) % 86400
    # 现在时间
    shijiancuo = int(time.time())
    # 今天日期
    today = datetime.date.today()
    # 昨天时间
    yesterday = today - datetime.timedelta(days=1)
    # 昨天开始时间戳
    yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
    # 昨天完成时间戳
    yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1

    username = g.current_member.username
    query = db.session.query(DfAgentRate.mer_username).filter(DfAgentRate.agent_name == username).all()

    times = 0
    real_amount_sum = 0
    ytimes = 0
    yreal_amount_sum = 0
    for i in query:
        user = i[0]
        res = db.session.query(
            func.coalesce(func.count(DfTradeDao.mer_username), 0).label('times'),
            func.coalesce(func.sum(DfTradeDao.amount), 0).label('real_amount_sum')).filter(DfTradeDao.state == 2,
                                                                                           DfTradeDao.mer_username == user,
                                                                                           zeroPoint <= DfTradeDao.action_time ,
                                                                                           DfTradeDao.action_time <= shijiancuo).all()
        times += res[0][0]
        real_amount_sum += res[0][1]

        args = db.session.query(
            func.coalesce(func.count(DfTradeDao.mer_username == user), 0).label('times'),
            func.coalesce(func.sum(DfTradeDao.amount), 0).label('real_amount_sum')).filter(
            yesterday_start_time <= DfTradeDao.action_time,
            DfTradeDao.mer_username == username, DfTradeDao.state == 2,
            DfTradeDao.action_time <= yesterday_end_time,
            DfTradeDao.mer_username == user).all()

        ytimes += args[0][0]
        yreal_amount_sum += args[0][1]


    data['number_day'] = times
    data["n_total_amount"] = float('%.2f' % real_amount_sum)
    data['number_yes'] = ytimes
    data["y_total_amount"] = float('%.2f' % yreal_amount_sum)
    result.append(data)
    return result