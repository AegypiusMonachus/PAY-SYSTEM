
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with,fields
from app.models.bank_trade_dao import BankTradeDao
from app.models.transaction_code_dao import Qrcode
from app.models import paginate
from app.models import db
from sqlalchemy import desc
from app.models.onlinetrades_dao import OnlinetradesDao



def get_data(critern=None,page=None,per_page=None):
    query = db.session.query(
        BankTradeDao.id,
        BankTradeDao.order_no,
        BankTradeDao.amount,
        BankTradeDao.action_time,
        BankTradeDao.pay_time,
        BankTradeDao.qr_code,
        BankTradeDao.state,
        BankTradeDao.audit_time,

    ).order_by(desc(BankTradeDao.action_time))
    res = paginate(query,critern,page,per_page)
    return res