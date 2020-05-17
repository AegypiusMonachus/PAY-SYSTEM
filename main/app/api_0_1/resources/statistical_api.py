from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.api_0_1.utils import DEFAULT_PAGE,DEFAULT_PAGE_SIZE
from app.api_0_1.common import make_response
from app.models import db
from sqlalchemy import and_,func
from decimal import *
from app.common import keep_two_del
from app.service.statistical_services import StaticSer
from app.models.refulation_dao import RefulationDao

from app.models.merchant_dao import MerchantDao
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.withdraw_dao import WithdrawDao
from app.models.df_trade_dao import DfTradeDao,DfTradeRechargeDao,DfTradeSxfDao
from app.models.df_agent_rate_dao import DfAgentRate

def tupinlist(fn):
    res_list = []
    for i in fn:
        i = list(i)
        res_list.append(i)
    return res_list

def data_d1(fn1, fn2):
    dict1 = {a[0]: a for a in fn1}
    dict2 = {a[0]: a for a in fn2}

    for i in fn1:
        for b in fn2:
            if b[0] in dict1 and b[0] == i[0]:
                dict1[i[0]].append(b[1])
                dict1[i[0]].append(b[2])
        if i[0] not in dict2:
            dict1[i[0]].append(0)
            dict1[i[0]].append(0)
    data_1 = list(dict1.values())
    return data_1

def data_d2(fn1, fn2):
    dict1 = {a[0]: a for a in fn1}
    dict2 = {a[0]: a for a in fn2}

    for i in fn1:
        for b in fn2:
            if b[0] in dict1 and b[0] == i[0]:
                dict1[i[0]].append(b[1])
        if i[0] not in dict2:
            dict1[i[0]].append(0)
    data_1 = list(dict1.values())
    return data_1

# 商户的统计报表
class StatisticalApi(Resource):
    def get(self):
        statisticalParsers = RequestParser(trim=True)
        statisticalParsers.add_argument('page', type=int, default=DEFAULT_PAGE)
        statisticalParsers.add_argument('page_size', type=int, default=DEFAULT_PAGE_SIZE)
        statisticalParsers.add_argument('qr_code', type=str)
        statisticalParsers.add_argument('name', type=str)
        statisticalParsers.add_argument('user_name', type=str)
        statisticalParsers.add_argument('state', type=int)
        statisticalParsers.add_argument('begin_time', type=int)
        statisticalParsers.add_argument('end_time', type=int)
        m_args = statisticalParsers.parse_args(strict=True)

        critern = set()
        if m_args['qr_code'] is not None:
            critern.add(OnlinetradesDao.qr_code == m_args['qr_code'])
        if m_args['name'] is not None:
            critern.add(OnlinetradesDao.drawee == m_args['name'])
        if m_args['user_name'] is not None:
            critern.add(OnlinetradesDao.user_name == m_args['user_name'])
        if m_args['state'] is not None:
            critern.add(OnlinetradesDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern.add(OnlinetradesDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(OnlinetradesDao.action_time <= m_args['end_time'])

        critern_w = set()
        # if m_args['order_no'] is not None:
        #     critern_w.add(WithdrawDao.order_no == m_args['order_no'])
        if m_args['name'] is not None:
            critern_w.add(WithdrawDao.name == m_args['name'])
        if m_args['user_name'] is not None:
            critern_w.add(WithdrawDao.user_name == m_args['user_name'])
        if m_args['state'] is not None:
            critern_w.add(WithdrawDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern_w.add(WithdrawDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern_w.add(WithdrawDao.action_time <= m_args['end_time'])

        res_total = db.session.query(
            OnlinetradesDao.mer_code,
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.amount).label('amount'),
            func.sum(OnlinetradesDao.real_cost_service).label('real_cost_service'),
            func.sum(OnlinetradesDao.real_cost_agent).label('real_cost_agent'),
            func.count(OnlinetradesDao.id).label('total_count')
        ).filter(*critern).group_by(OnlinetradesDao.mer_code, OnlinetradesDao.user_name).all()
        res_total_list = tupinlist(res_total)

        res_wq1 = db.session.query(
            OnlinetradesDao.mer_code,
            func.sum(OnlinetradesDao.amount).label('wq_amount'),
            func.count(OnlinetradesDao.id).label('wq_total_count')
        ).filter(*critern, OnlinetradesDao.state == 1).group_by(OnlinetradesDao.mer_code).all()
        res_wq1_list = tupinlist(res_wq1)

        res_wq2 = db.session.query(
            WithdrawDao.mer_code,
            func.sum(WithdrawDao.paid_amount).label('w_paid_amount')
        ).filter(*critern_w, WithdrawDao.state == 1).group_by(WithdrawDao.mer_code).all()
        res_wq2_list = tupinlist(res_wq2)

        res_q1 = db.session.query(
            OnlinetradesDao.mer_code,
            func.sum(OnlinetradesDao.bank_amount).label('q_amount'),
            func.count(OnlinetradesDao.id).label('q_total_count')
        ).filter(*critern, OnlinetradesDao.state == 2).group_by(OnlinetradesDao.mer_code).all()
        res_q1_list = tupinlist(res_q1)

        res_q2 = db.session.query(
            WithdrawDao.mer_code,
            func.sum(WithdrawDao.paid_amount).label('q_paid_amount'),
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount')
        ).filter(*critern_w, WithdrawDao.state == 2).group_by(WithdrawDao.mer_code).all()
        res_q2_list = tupinlist(res_q2)

        data_1 = data_d1(res_total_list, res_wq1_list)
        data_2 = data_d2(data_1, res_wq2_list)
        data_3 = data_d1(data_2, res_q1_list)
        data_4 = data_d1(data_3, res_q2_list)

        result = []
        for data in data_4:
            if data[3]:
                data_1 = data[3]
            else:
                data_1 = Decimal(0)
            if data[4]:
                data_2 = data[4]
            else:
                data_2 = Decimal(0)
            if data[6]:
                data_3 = data[6]
            else:
                data_3 = Decimal(0)
            if data[9]:
                data_4 = data[9]
            else:
                data_4 = Decimal(0)
            if data[12]:
                data_5 = data[12]
            else:
                data_5 = Decimal(0)
            if data[8]:
                data_6 = data[8]
            else:
                data_6 = Decimal(0)
            if data[11]:
                data_7 = data[11]
            else:
                data_7 = Decimal(0)

            result.append({
                "user_name": data[1],
                "total_amount": float(keep_two_del(data_3+data_4)),     # 交易金额
                "cost_service": float(keep_two_del(data_1)),  # 服务费
                "cost_agent": float(keep_two_del(data_2)),  # 代理费
                "total_count": data[5],  # 总计
                "wq_amount": float(keep_two_del(data_3)),       # 未确认
                "wq_total_count": data[7],  # 未完成数
                "w_paid_amount": float(keep_two_del(data_6)),    # 代付未完成
                "q_amount": float(keep_two_del(data_4)),  # 确认
                "q_total_count": data[10],  # 已完成数
                "q_paid_amount": float(keep_two_del(data_7)),  # 代付已完成
                "shouxu":float(keep_two_del(data_1+data_5))
            })

        return make_response(result)


# 平台的统计报表
class StatisticalKkApi(Resource):
    def get(self):
        statisticalParsers = RequestParser(trim=True)
        statisticalParsers.add_argument('state', type=int)
        statisticalParsers.add_argument('begin_time', type=int)
        statisticalParsers.add_argument('end_time', type=int)
        m_args = statisticalParsers.parse_args(strict=True)

        critern = set()
        critern_jiaoyi = set()
        critern_tx = set()
        critern_xinyong = set()
        critern_df = set()
        critern_sxf = set()
        if m_args['state'] is not None:
            critern_jiaoyi.add(OnlinetradesDao.state == m_args['state'])
            critern_tx.add(WithdrawDao.state == m_args['state'])
            critern_xinyong.add(DfTradeRechargeDao.state == m_args['state'])
            critern_df.add(DfTradeDao.state == m_args['state'])
        if m_args['begin_time'] is not None:
            critern_jiaoyi.add(OnlinetradesDao.action_time >= m_args['begin_time'])
            critern_tx.add(WithdrawDao.action_time >= m_args['begin_time'])
            critern_xinyong.add(DfTradeRechargeDao.action_time >= m_args['begin_time'])
            critern_df.add(DfTradeDao.action_time >= m_args['begin_time'])
            critern_sxf.add(DfTradeSxfDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern_jiaoyi.add(OnlinetradesDao.action_time <= m_args['end_time'])
            critern_tx.add(WithdrawDao.action_time <= m_args['end_time'])
            critern_xinyong.add(DfTradeRechargeDao.action_time <= m_args['end_time'])
            critern_df.add(DfTradeDao.action_time <= m_args['end_time'])
            critern_sxf.add(DfTradeSxfDao.action_time <= m_args['end_time'])


        agents_name = db.session.query(RefulationDao.agents).first()
        if agents_name is not None:
            res = db.session.query(DfAgentRate.mer_username).filter(DfAgentRate.agent_name == agents_name.agents).all()
            result = []
            for i in res:
                result.append(i[0])
            critern_xinyong.add(DfTradeRechargeDao.username.in_(result))
            critern_df.add(DfTradeDao.mer_username.in_(result))
            critern.add(MerchantDao.parent_name == agents_name.agents)
            critern_sxf.add(DfTradeSxfDao.agents_username == agents_name.agents)

        res_args = StaticSer().get_date(critern = critern,critern_jiaoyi = critern_jiaoyi,critern_tx = critern_tx,critern_xinyong = critern_xinyong,critern_df = critern_df,critern_sxf = critern_sxf)
        result = []
        for res in res_args:

            if res.xinyong_amount is not None:
                xinyong_amount = float('%.2f' % keep_two_del(res.xinyong_amount))
            else:
                xinyong_amount = 0



            if res.dfjiaoyi_amount is not None:
                dfjiaoyi_amount = float('%.2f' % keep_two_del(res.dfjiaoyi_amount))
            else:
                dfjiaoyi_amount = 0



            if res.wraw_amount is not None:
                wraw_amount = float('%.2f' % keep_two_del(res.wraw_amount))
            else:
                wraw_amount = 0

            if res.wrdraw_amount_sxf is not None:
                wrdraw_amount_sxf = float('%.2f' % keep_two_del(res.wrdraw_amount_sxf))
            else:
                wrdraw_amount_sxf = 0


            if res.jiaoyi_amount is not None:
                jiaoyi_amount = float('%.2f' % keep_two_del(res.jiaoyi_amount))
            else:
                jiaoyi_amount = 0

            if res.jiaoyi_amount_service is not None:
                jiaoyi_amount_service = float('%.2f' % keep_two_del(res.jiaoyi_amount_service))
            else:
                jiaoyi_amount_service = 0

            if res.jiaoyi_amount_agents is not None:
                jiaoyi_amount_agents = float('%.2f' % keep_two_del(res.jiaoyi_amount_agents))
            else:
                jiaoyi_amount_agents = 0

            if res.df_sxf is not None:
                df_sxf = float('%.2f' % keep_two_del(res.df_sxf))
            else:
                df_sxf = 0

            if res.sunyi is not None:
                sunyi = float('%.2f' % keep_two_del(res.sunyi))
            else:
                sunyi = 0


            result.append({
                'xinyong_num': res.xinyong_num,
                'xinyong_amount': xinyong_amount,
                'dfjiaoyi_num': res.dfjiaoyi_num,
                'dfjiaoyi_amount': dfjiaoyi_amount,
                'wraw_num': res.wraw_num,
                'wraw_amount': wraw_amount,
                'wrdraw_amount_sxf': wrdraw_amount_sxf,
                'jiaoyi_num': res.jiaoyi_num,
                'jiaoyi_amount': jiaoyi_amount,
                'jiaoyi_amount_service': jiaoyi_amount_service,
                'jiaoyi_amount_agents': jiaoyi_amount_agents,
                'df_sxf': df_sxf,
                'sunyi': sunyi,

            })

        return make_response(result)
