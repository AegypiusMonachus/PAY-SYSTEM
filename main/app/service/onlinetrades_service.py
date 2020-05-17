from app.models import db
from ..models.onlinetrades_dao import OnlinetradesDao
from ..models.merchant_dao import MerchantBank,MerchantDao,PayType
from app.models.withdraw_dao import WithdrawDao,BankDao
from app.models.transaction_code_dao import Qrcode
from app.models.onlinetrade_confirm import OnlineTradeConfirmDao
from sqlalchemy import and_,func
from app.api_0_1.utils import SECONDS_PER_DAY
import time,datetime
from flask import g
from app.models.refulation_dao import RefulationDao
from decimal import Decimal


def getOnlineData(args,page=None,per_page=None):
    res = db.session.query(
        OnlinetradesDao.order_no.label('order_no'),
        OnlinetradesDao.user_name.label('user_name'),
        OnlinetradesDao.org_order_no.label('org_order_no'),
        OnlinetradesDao.bank_order_no.label('bank_order_no'),
        OnlinetradesDao.qr_code.label('qr_code'),
        OnlinetradesDao.amount.label('amount'),
        OnlinetradesDao.real_amount.label('real_amount'),
        OnlinetradesDao.action_time.label('action_time'),
        OnlinetradesDao.mer_code.label('mer_code'),
        OnlinetradesDao.pay_type.label('pay_type'),
        OnlinetradesDao.cost_service.label('cost_service'),
        OnlinetradesDao.cost_agent.label('cost_agent'),
        OnlinetradesDao.audit_time.label('audit_time'),
        OnlinetradesDao.state.label('state'),
        OnlinetradesDao.remark.label('remark'),
        OnlinetradesDao.mer_ip.label('mer_ip'),
        OnlinetradesDao.match_type.label('match_type'),
        OnlinetradesDao.bank_amount,
        OnlinetradesDao.discount_amount,
        OnlinetradesDao.real_cost_service,
        OnlinetradesDao.real_cost_agent,
        BankDao.name.label('bank_name'),
        PayType.name.label('pay_type_name'),
        MerchantDao.parent_name.label('agents_name'),
        OnlineTradeConfirmDao.amount.label('amount_confirm'),
        OnlineTradeConfirmDao.qr_code.label('qr_code_confirm'),
        OnlineTradeConfirmDao.audit_time.label('audit_time_confirm'),
        OnlineTradeConfirmDao.cost_service.label('cost_service_confirm'),
        OnlineTradeConfirmDao.cost_agent.label('cost_agent_confirm'),
        OnlineTradeConfirmDao.administrator.label('administrator_confirm'),
    ).filter(*args).order_by(OnlinetradesDao.action_time.desc())
    res = res.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
    res = res.outerjoin(OnlineTradeConfirmDao, and_(OnlinetradesDao.order_no == OnlineTradeConfirmDao.order_no,OnlinetradesDao.bank_order_no == OnlineTradeConfirmDao.bank_order_no))
    res = res.outerjoin(PayType, OnlinetradesDao.pay_type == PayType.type)
    res = res.outerjoin(Qrcode, Qrcode.code == OnlinetradesDao.qr_code)
    res = res.outerjoin(BankDao, Qrcode.bank_id == BankDao.id)

    res = res.paginate(page, per_page, error_out=False)
    return res

def getOnlineDateByCountOrderNo(orderno):
    return db.session.query(OnlinetradesDao).filter(OnlinetradesDao.org_order_no == orderno).count()


def get_online_data_datil():
    if g.current_member:
        username = g.current_member.username
    else:
        return {
            'success': False,
            'errorCode': 402,
            'errorMsg': '请登录'
        }
    res = db.session.query(
        OnlinetradesDao.mer_code.label('mer_code'),
        func.sum(OnlinetradesDao.amount).label('sum_amount')
    ).filter(and_(OnlinetradesDao.user_name == username,OnlinetradesDao.state == 2)).group_by(OnlinetradesDao.mer_code)
    res = res.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
    res = res.first()

    return res


def get_online_data_datil_amount():
    if g.current_member:
        username = g.current_member.username
    else:
        return {
            'success': False,
            'errorCode': 402,
            'errorMsg': '请登录'
        }
    res = db.session.query(
        MerchantDao.amount
    ).filter(MerchantDao.username == username)
    res = res.first()

    return res


def get_online_data_datil_amount_number():
    if g.current_member:
        username = g.current_member.username
    else:
        return {
            'success': False,
            'errorCode': 402,
            'errorMsg': '请登录'
        }
    res = db.session.query(
        func.count(OnlinetradesDao.id).label('number')
    ).filter(OnlinetradesDao.user_name == username).filter(OnlinetradesDao.state == 2).group_by(OnlinetradesDao.user_name)
    res = res.first()

    return res


def get_online_data_datil_day():
    if g.current_member:
        username = g.current_member.username
    else:
        return {
            'success': False,
            'errorCode': 402,
            'errorMsg': '请登录'
        }
    today = datetime.date.today()
    zeroPointToday = int(time.mktime(today.timetuple()))
    endPointToday = zeroPointToday + SECONDS_PER_DAY
    res = db.session.query(
        func.sum(OnlinetradesDao.bank_amount).label('sum_amount_day'),
        func.count(OnlinetradesDao.id).label('number_day'),
    ).filter(and_(
        OnlinetradesDao.user_name == username,
        OnlinetradesDao.state == 2,
        OnlinetradesDao.audit_time >= zeroPointToday,
        OnlinetradesDao.audit_time < endPointToday
    )).group_by(OnlinetradesDao.mer_code)
    res = res.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
    res = res.first()
    return res

def get_online_data_datil_yes():
    if g.current_member:
        username = g.current_member.username
    else:
        return {
            'success': False,
            'errorCode': 402,
            'errorMsg': '请登录'
        }
    '''昨日时间'''
    today = datetime.date.today()
    zeroPointToday = int(time.mktime(today.timetuple()))
    endPointToday = zeroPointToday + SECONDS_PER_DAY
    endPointYestoday = zeroPointToday
    # print('昨日%s' % endPointYestoday)
    zeroPointYestoday = endPointYestoday - 60 * 60 * 24
    res = db.session.query(
        func.sum(OnlinetradesDao.bank_amount).label('sum_amount_yes'),
        func.count(OnlinetradesDao.id).label('number_yes'),
    ).filter(and_(
        OnlinetradesDao.user_name == username,
        OnlinetradesDao.state == 2,
        OnlinetradesDao.audit_time >= zeroPointYestoday,
        OnlinetradesDao.audit_time < endPointYestoday
    )).group_by(OnlinetradesDao.mer_code)
    res = res.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
    res = res.first()
    return res



def getonline_total(args):
    res = db.session.query(
        func.coalesce(func.sum(OnlinetradesDao.amount),0).label('amount_sum'),
        func.coalesce(func.sum(OnlinetradesDao.bank_amount),0).label('real_amount_sum'),
        func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('rcs_sum'),
        func.coalesce(func.sum(OnlinetradesDao.real_cost_agent),0).label('rca_sum'),
    ).filter(*args)
    res = res.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
    res = res.outerjoin(OnlineTradeConfirmDao, and_(OnlinetradesDao.order_no == OnlineTradeConfirmDao.order_no,OnlinetradesDao.bank_order_no == OnlineTradeConfirmDao.bank_order_no))
    res = res.outerjoin(PayType, OnlinetradesDao.pay_type == PayType.type)
    res = res.outerjoin(Qrcode, Qrcode.code == OnlinetradesDao.qr_code)
    res = res.outerjoin(BankDao, Qrcode.bank_id == BankDao.id)

    res = res.all()
    return res

def getonline_total_mem(args):
    res = db.session.query(
        func.coalesce(func.sum(OnlinetradesDao.amount),0).label('amount_sum'),
        func.coalesce(func.sum(OnlinetradesDao.bank_amount),0).label('real_amount_sum'),
        func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('rcs_sum')
    ).filter(*args)
    res = res.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
    res = res.outerjoin(OnlineTradeConfirmDao, and_(OnlinetradesDao.order_no == OnlineTradeConfirmDao.order_no,OnlinetradesDao.bank_order_no == OnlineTradeConfirmDao.bank_order_no))
    res = res.outerjoin(PayType, OnlinetradesDao.pay_type == PayType.type)
    res = res.outerjoin(Qrcode, Qrcode.code == OnlinetradesDao.qr_code)
    res = res.outerjoin(BankDao, Qrcode.bank_id == BankDao.id)

    res = res.all()
    return res

# 单条订单手续费和代理费计算
def get_online_cost(order):
    # arg_01 = db.session.query(OnlinetradesDao).filter(OnlinetradesDao.order_no == args['order_no']).first()
    bank_amount = order.bank_amount

    username = order.user_name
    merchant = db.session.query(MerchantDao).filter(MerchantDao.username == username).first()
    rate = None
    for k, v in merchant.rate.items():
        if int(k) == order.pay_type:
            rate = v
            break
        else:
            rate = 0
    cost_service = bank_amount * Decimal(rate) / 100

    def_agent = db.session.query(RefulationDao.agents).scalar()
    if def_agent == merchant.parent_name:
        cost_agent = Decimal(0)
    else:
        agent_rate = db.session.query(MerchantDao.rate).filter(MerchantDao.username == merchant.parent_name).scalar()
        rate_a = None
        if agent_rate:
            for k, v in agent_rate.items():
                if int(k) == order.pay_type:
                    rate_a = v
                    break
                else:
                    rate_a = 0
            cost_agent = bank_amount * (Decimal(rate) - Decimal(rate_a)) / 100
        else:
            cost_agent = Decimal(0)

    result = []
    result.append({
        "cost_service": float(cost_service),
        "cost_agent": float(cost_agent),
        "amount": float(order.amount),
        "discount_amount": float(order.discount_amount),
        "real_amount": float(order.real_amount),    # 申请金额与随机减免的差值
        "bank_amount": float(order.bank_amount)     # 银行回调金额
    })
    return result
