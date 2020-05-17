from app.models import db
from app.models.withdraw_dao import WithdrawDao,BankDao
from app.models.merchant_dao import MerchantBank,MerchantInfo,MerchantDao,PayType
from app.models.user_dao import UserDao
from flask_restful import abort
import time
from flask import g
from app.service.serviceutils.utils import makeOrder
from sqlalchemy import and_,func
from app.models.transaction_code_dao import Qrcode
from app.models.onlinetrade_confirm import OnlineTradeConfirmDao
from decimal import Decimal


def getOnlineData(args,page=None,per_page=None):
    res = db.session.query(
        WithdrawDao.mer_code,
        MerchantDao.username,
        WithdrawDao.order_no,
        WithdrawDao.bank_id,
        BankDao.name.label('bank_name'),
        WithdrawDao.amount,
        WithdrawDao.wrdraw_amount,
        WithdrawDao.paid_amount,
        WithdrawDao.real_amount,
        WithdrawDao.action_time,
        WithdrawDao.audit_time,
        WithdrawDao.state,
        WithdrawDao.cost_sx,
        WithdrawDao.mer_ip,
        WithdrawDao.remark,
        WithdrawDao.account,
        WithdrawDao.name,
        UserDao.username.label('audit_name')


    ).filter(*args).order_by(WithdrawDao.action_time.desc())
    res = res.outerjoin(BankDao,WithdrawDao.bank_id == BankDao.id)
    res = res.outerjoin(MerchantInfo, WithdrawDao.mer_code == MerchantInfo.code)
    res = res.outerjoin(MerchantDao, WithdrawDao.mer_code == MerchantDao.code)
    res = res.outerjoin(UserDao, UserDao.id == WithdrawDao.audit_user)
    res = res.paginate(page, per_page, error_out=False)
    return res


def insert(m_args):
    if g.current_member:
        username = g.current_member.username
    else:
        username = 'zzz123'

    res = db.session.query(MerchantDao.id,MerchantDao.code,MerchantDao.amount,MerchantDao.dongjie_amount,MerchantDao.wrdraw_amount).filter(MerchantDao.username == username).first()

    if res is not None:
        id = res.id
        code = res.code
        if res.amount < m_args['amount']:
            return {
                'success': False,
                'errorCode': 404,
                'errorMsg': '取款金额不能大于用户余额'
            }
    else:
        return {
                'success':False,
                'errorCode': 403,
                'errorMsg': '该用户不存在'
                }


    m_args['order_no'] = makeOrder(id)
    m_args['state'] = 1
    m_args['action_time'] = int(time.time())
    m_args['mer_code'] = code
    m_args['mer_name'] = username
    m_args['wrdraw_amount'] = res.wrdraw_amount
    m_args['paid_amount'] = Decimal(m_args['amount']) + m_args['wrdraw_amount']


    args = {}
    args['amount'] = res.amount - m_args['paid_amount']
    if res.wrdraw_amount is None:
        res.wrdraw_amount = 0
    args['dongjie_amount'] = Decimal(m_args['amount']) + res.wrdraw_amount

    try:
        dao = MerchantDao.query.filter(MerchantDao.username == username).update(args)
        w_dao = WithdrawDao(**m_args)
        db.session.add(w_dao)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)

def getstate(ord_no):
    res = db.session.query(WithdrawDao.state).filter(WithdrawDao.order_no == ord_no).first()
    return res

def update(m_args):
    with_dao = db.session.query(WithdrawDao.mer_code,WithdrawDao.amount,WithdrawDao.paid_amount).filter(WithdrawDao.order_no == m_args['order_no']).first()

    if with_dao is not None:
        res = db.session.query(MerchantDao.amount,MerchantDao.dongjie_amount).filter(MerchantDao.code == with_dao.mer_code).first()

    else:
        return {
            'success': False,
            'errorCode': 403,
            'errorMsg': '该订单不存在'
        }


    m_args['audit_user'] = 1
    m_args['audit_time'] = int(time.time())


    args = {}
    if m_args['state'] == 2:
        args['dongjie_amount'] = res.dongjie_amount - with_dao.paid_amount
    elif m_args['state'] == 3:

        args['dongjie_amount'] =  res.dongjie_amount - with_dao.paid_amount
        args['amount'] = res.amount + res.dongjie_amount
    try:
        WithdrawDao.query.filter(WithdrawDao.order_no == m_args['order_no']).update(m_args)
        dao = MerchantDao.query.filter(MerchantDao.code == with_dao.mer_code).update(args)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)



def getwithdraw_total(args):
    res = db.session.query(
        func.sum(WithdrawDao.amount).label('amount_sum'),
        func.sum(WithdrawDao.paid_amount).label('paid_amount'),
        func.sum(WithdrawDao.wrdraw_amount).label('withdraw_amount_sum')
    ).filter(*args)
    res = res.outerjoin(BankDao, WithdrawDao.bank_id == BankDao.id)
    res = res.outerjoin(MerchantInfo, WithdrawDao.mer_code == MerchantInfo.code)
    res = res.outerjoin(MerchantDao, WithdrawDao.mer_code == MerchantDao.code)
    res = res.outerjoin(UserDao, UserDao.id == WithdrawDao.audit_user)
    res = res.all()
    return res

