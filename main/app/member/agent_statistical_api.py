from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.api_0_1.utils import DEFAULT_PAGE,DEFAULT_PAGE_SIZE
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.withdraw_dao import WithdrawDao
from app.models.merchant_dao import MerchantDao
from app.api_0_1.common import make_response
from app.models import db
from sqlalchemy import and_,func
from flask import g
from app.common import keep_two_del


# 商户的统计报表
class AgentStatisticalApi(Resource):
    def get(self):
        statisticalParsers = RequestParser(trim=True)
        statisticalParsers.add_argument('page', type=int, default=DEFAULT_PAGE)
        statisticalParsers.add_argument('page_size', type=int, default=DEFAULT_PAGE_SIZE)
        statisticalParsers.add_argument('user_name', type=str)
        statisticalParsers.add_argument('begin_time', type=int)
        statisticalParsers.add_argument('end_time', type=int)
        m_args = statisticalParsers.parse_args(strict=True)

        critern = set()
        if m_args['user_name'] is not None:
            critern.add(OnlinetradesDao.user_name == m_args['user_name'])
        if m_args['begin_time'] is not None:
            critern.add(OnlinetradesDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(OnlinetradesDao.action_time <= m_args['end_time'])

        critern_w = set()
        # if m_args['order_no'] is not None:
        #     critern_w.add(WithdrawDao.order_no == m_args['order_no'])
        if m_args['user_name'] is not None:
            critern_w.add(WithdrawDao.user_name == m_args['user_name'])
        if m_args['begin_time'] is not None:
            critern_w.add(WithdrawDao.action_time >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern_w.add(WithdrawDao.action_time <= m_args['end_time'])

        if g.current_member:
            username = g.current_member.username
            res_merchant = db.session.query(MerchantDao).filter(MerchantDao.username==username).first()
            res_merchant_list = db.session.query(MerchantDao).filter(MerchantDao.parent_name==username).all()
            res_list = []
            for i in res_merchant_list:
                res_list.append(i.code)

            if res_merchant.type==2:
                res_total = db.session.query(
                    OnlinetradesDao.mer_code,
                    OnlinetradesDao.user_name,
                    func.sum(OnlinetradesDao.bank_amount).label('amount'),
                    func.sum(OnlinetradesDao.real_cost_agent).label('real_cost_agent')
                ).filter(*critern, OnlinetradesDao.state==2).group_by(OnlinetradesDao.mer_code, OnlinetradesDao.user_name).all()

                res_total_list = []
                for i in res_total:
                    if i.mer_code in res_list:
                        res_total_list.append(i)

                result = []
                for data in res_total_list:

                    result.append({
                        "user_name": data.user_name,
                        "total_amount": float(keep_two_del(data.amount)),  # 交易金额
                        "cost_agent": float(keep_two_del(data.real_cost_agent))  # 代理费
                    })
                return make_response(result)
            else:
                return {'success': False, 'errorMsg': '您不是代理'}
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }







