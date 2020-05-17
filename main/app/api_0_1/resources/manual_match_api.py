from ..common import make_response
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.bank_trade_dao import BankTradeDao
from app.models.merchant_dao import MerchantDao
from app.models.onlinetrade_confirm import OnlineTradeConfirmDao
from app.models.refulation_dao import RefulationDao
from app.models.user_dao import UserDao
from app.models import db
import time
from app.extensions import code_manager
from flask import g
from decimal import Decimal
from app.common import keep_two_del


'''人工匹配'''

class ManualMatchApi(Resource):
    def put(self):
        parser = RequestParser(trim=True)
        parser.add_argument('order_no', type=int)
        parser.add_argument('order_id', type=int)
        parser.add_argument('password', type=str)
        args = parser.parse_args(strict=True)

        if g.current_member:
            username = g.current_member.username
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }

        res_pass = db.session.query(UserDao.password).filter(UserDao.username==username).first()

        if args['password'] == res_pass[0]:
            bank = db.session.query(BankTradeDao).filter(BankTradeDao.order_no==args['order_no']).first()
            online = db.session.query(OnlinetradesDao).filter(OnlinetradesDao.order_no==args['order_id']).first()

            time_t = int(time.time())
            if bank and online:
                if bank.state==1 and online.state==1:
                    merchant = db.session.query(MerchantDao).filter(MerchantDao.username==online.user_name).first()
                    rate = None
                    for k,v in merchant.rate.items():
                        if int(k) == online.pay_type:
                            rate = v
                            break
                        else:
                            rate = 0
                    cost_service = bank.amount * Decimal(rate) / 100
                    def_agent = db.session.query(RefulationDao.agents).scalar()

                    if def_agent == merchant.parent_name:
                        cost_agent = Decimal(0)
                    else :
                        agent_rate = db.session.query(MerchantDao.rate).filter(MerchantDao.username == merchant.parent_name).scalar()
                        rate_a = None
                        if agent_rate:
                            for k, v in agent_rate.items():
                                if int(k) == online.pay_type:
                                    rate_a = v
                                    break
                                else:
                                    rate_a = 0
                            cost_agent = bank.amount * (Decimal(rate) - Decimal(rate_a)) / 100
                        else:
                            cost_agent = Decimal(0)
                    merchant_agent = db.session.query(MerchantDao).filter(MerchantDao.username==merchant.parent_name).first()
                    merchant_agent.amount = merchant_agent.amount + cost_agent

                    merchant.amount = merchant.amount + bank.amount - cost_service
                    bank.state = 2
                    bank.audit_time = time_t
                    online.state = 2
                    online.bank_order_no = args['order_no']
                    online.match_type = 1
                    online.bank_amount = bank.amount
                    # 存入额度确认表tb_onlinetrade_confirm
                    onlinetrade_confirm = OnlineTradeConfirmDao()
                    onlinetrade_confirm.order_no = online.order_no
                    onlinetrade_confirm.bank_order_no = bank.order_no
                    onlinetrade_confirm.amount = bank.amount
                    onlinetrade_confirm.qr_code = bank.qr_code
                    onlinetrade_confirm.audit_time = time_t
                    onlinetrade_confirm.cost_service = cost_service
                    onlinetrade_confirm.cost_agent = cost_agent
                    onlinetrade_confirm.mer_code = online.mer_code
                    onlinetrade_confirm.administrator = username # 全局g对象获取管理员
                    online.real_cost_service = cost_service
                    online.real_cost_agent = cost_agent
                    online.bank_amount = bank.amount
                    online.audit_time = int(time.time())
                    try:
                        db.session.add(bank)
                        db.session.add(online)
                        db.session.add(onlinetrade_confirm)
                        db.session.add(merchant)
                        db.session.add(merchant_agent)
                        db.session.commit()
                        try:
                            import requests
                            requests.get('http://127.0.0.1:8125/main/payManual', timeout=2)
                        except:
                            pass
                    except:
                        db.session.rollback()
                        db.session.remove()

                    finally:
                        code_manager.finish(bank.qr_code, online.amount, online.discount_amount, bank.amount)
                    return {'success': True}
                else:
                    return {'success': False, 'errorMsg': "您输入的订单号不是交易中！"}
            else:
                return {'success': False}
        else:
            return {'success': False, 'errorMsg': "您输入的密码不正确"}


class ManualMatchDetailApi(Resource):
    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('order_no', type=int)
        args = parser.parse_args(strict=True)

        # cost_detail = db.session.query(OnlineTradeConfirmDao).filter(OnlineTradeConfirmDao.order_no==1567578191100112352).first()
        cost_detail = db.session.query(OnlineTradeConfirmDao).filter(OnlineTradeConfirmDao.order_no==args['order_no']).first()
        result = []
        result.append({
            "id": cost_detail.id,
            "order_no":cost_detail.order_no,
            "bank_order_no":cost_detail.bank_order_no,
            "amount": float(keep_two_del(cost_detail.amount)),
            "cost_service": float(keep_two_del(cost_detail.cost_service)),
            "cost_agent": float(keep_two_del(cost_detail.cost_agent))
        })

        return result

