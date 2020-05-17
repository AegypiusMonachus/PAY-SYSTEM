from app.models import db
from ..models.onlinetrades_dao import OnlinetradesDao
from ..models.merchant_dao import MerchantBank,MerchantDao,PayType
from sqlalchemy import and_,func
from app.api_0_1.utils import SECONDS_PER_DAY
import time,datetime
from flask import g
from app.models.refulation_dao import RefulationDao
from app.models.df_trade_dao import DfTradeDao,DfTradeSxfDao
from app.models.withdraw_dao import BankDao
from app.models.df_agent_rate_dao import DfAgentRate


def getOnlineData(args,page=None,per_page=None):
    res = db.session.query(
        DfTradeDao.id.label('id'),
        DfTradeDao.order_no.label('order_no'),
        DfTradeDao.org_order_no.label('org_order_no'),
        DfTradeDao.mer_code.label('mer_code'),
        DfTradeDao.mer_username.label('mer_username'),
        DfTradeDao.amount.label('amount'),
        DfTradeDao.action_time.label('action_time'),
        DfTradeDao.audit_time.label('audit_time'),
        DfTradeDao.real_sxf.label('sxf'),
        DfTradeDao.state.label('state'),
        DfTradeDao.type.label('type'),
        DfTradeDao.bank_id.label('bank_id'),
        DfTradeDao.account_name.label('account_name'),
        DfTradeDao.account_no.label('account_no'),
        DfTradeDao.sxf_detail.label('sxf_detail'),
        BankDao.name.label('bank_name')
    ).filter(*args).order_by(DfTradeDao.action_time.desc())
    res = res.outerjoin(BankDao,DfTradeDao.bank_id == BankDao.id)
    res = res.outerjoin(MerchantDao, MerchantDao.username == DfTradeDao.mer_username)
    res = res.paginate(page, per_page, error_out=False)
    return res


def getOnlineDataTotal(args):
    res = db.session.query(
        func.sum(DfTradeDao.amount).label('amount'),
        func.sum(DfTradeDao.real_sxf).label('sxf')
    ).filter(*args).order_by(DfTradeDao.action_time.desc())
    res = res.outerjoin(BankDao,DfTradeDao.bank_id == BankDao.id)
    res = res.outerjoin(MerchantDao, MerchantDao.username == DfTradeDao.mer_username)
    res = res.all()
    return res


def getOnlineMerData(args,page=None,per_page=None):
    res = db.session.query(
        DfTradeDao.id.label('id'),
        DfTradeDao.order_no.label('order_no'),
        DfTradeDao.org_order_no.label('org_order_no'),
        DfTradeDao.mer_code.label('mer_code'),
        DfTradeDao.mer_username.label('mer_username'),
        DfTradeDao.amount.label('amount'),
        DfTradeDao.action_time.label('action_time'),
        DfTradeDao.audit_time.label('audit_time'),
        DfTradeDao.real_sxf.label('sxf'),
        DfTradeDao.state.label('state'),
        DfTradeDao.type.label('type'),
        DfTradeDao.bank_id.label('bank_id'),
        DfTradeDao.account_name.label('account_name'),
        DfTradeDao.account_no.label('account_no'),
        BankDao.name.label('bank_name')
    ).filter(*args).order_by(DfTradeDao.action_time.desc())
    res = res.outerjoin(BankDao,DfTradeDao.bank_id == BankDao.id)
    res = res.outerjoin(MerchantDao, MerchantDao.username == DfTradeDao.mer_username)
    res = res.paginate(page, per_page, error_out=False)
    return res



def getOnlineAgentsData(args,page=None,per_page=None):
    res = db.session.query(
        DfTradeDao.id.label('id'),
        DfTradeDao.order_no.label('order_no'),
        DfTradeDao.org_order_no.label('org_order_no'),
        DfTradeDao.mer_code.label('mer_code'),
        DfTradeDao.mer_username.label('mer_username'),
        DfTradeDao.amount.label('amount'),
        DfTradeDao.action_time.label('action_time'),
        DfTradeDao.audit_time.label('audit_time'),
        DfTradeDao.real_sxf.label('sxf'),
        DfTradeDao.state.label('state'),
        DfTradeDao.type.label('type'),
        DfTradeDao.bank_id.label('bank_id'),
        DfTradeDao.account_name.label('account_name'),
        DfTradeDao.account_no.label('account_no'),
        DfTradeDao.sxf_detail.label('sxf_detail'),
        BankDao.name.label('bank_name')
    ).filter(*args).order_by(DfTradeDao.action_time.desc())
    res = res.outerjoin(BankDao,DfTradeDao.bank_id == BankDao.id)
    res = res.outerjoin(MerchantDao, MerchantDao.username == DfTradeDao.mer_username)
    res = res.paginate(page, per_page, error_out=False)
    return res


def getOnlineDataAgentsTotal(args,args_sxf):
    res_amount = db.session.query(
        func.sum(DfTradeDao.amount).label('amount')
    ).filter(*args)
    res_amount = res_amount.subquery()

    res_order = db.session.query(DfTradeDao.order_no).filter(*args).all()
    orders = []
    if res_order is not None:
        for i in res_order:
            if i is not None:
                orders.append(i.order_no)

    res_sxf = db.session.query(
        func.sum(DfTradeSxfDao.sxf).label('sxf')
    ).filter(*args_sxf).filter(DfTradeSxfDao.order_no.in_(orders))
    res_sxf = res_sxf.subquery()

    res = db.session.query(
        res_amount.c.amount.label('amount'),
        res_sxf.c.sxf.label('sxf')
    )
    res = res.all()

    return res