from app.models.bank_trade_dao import BankTradeDao
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.merchant_dao import MerchantDao
from app.models.transaction_code_dao import Qrcode
from app.models import db
from app.log import banklogger 
import time,json
from decimal import *
from app.extensions import code_manager
from app.service.getsend_service import GetsendService
'''
Created on 2019年8月30日

@author: ly
'''
def bankNotify(qrid,args):
    #1:验证和保存回调数据
    qrcode = db.session.query(Qrcode.code).filter(Qrcode.id == qrid).scalar()
    mcount = db.session.query(BankTradeDao.id).filter(
        BankTradeDao.qr_code == qrcode, BankTradeDao.order_no == args['order_no']).count()
    if mcount != 0:
        banklogger.error("bankNotify订单号重复:%s"%(args['order_no']))
        return True;
    
    margs = {};
    margs['order_no'] = args['order_no']
    margs['amount'] = args['amount']
    margs['pay_time'] = args['pay_time']
    margs['qr_code'] = qrcode
    margs['action_time'] = int(time.time())
    margs['state'] = 1
    try:
        dao = BankTradeDao(**margs)
        dao.expansion_data = json.dumps(args)
        db.session.add(dao)
        db.session.commit()
        try:
            import requests
            requests.get('http://127.0.0.1:8125/main/bankCallback', timeout=2)
        except:
            pass
    except Exception as e:
        db.session.rollback()
        db.session.remove()
        banklogger.exception(e)
        banklogger.error("banktrade保存失败:%s"%(args))
        return
    #2:与交易记录匹配    
    try:
        matchOrder(dao);
        try:
            import requests
            requests.get('http://127.0.0.1:8125/main/payAutomatic', timeout=2)
        except:
            pass
    except Exception as e:
        banklogger.exception(e)
        banklogger.error("banktrade匹配失败:%s"%(args))
        return
        
def matchOrder(btradeDao):
    mtime = int(time.time())
    #1：根据qrcode和金额查询是否唯一
    otradeList = db.session.query(OnlinetradesDao).filter(OnlinetradesDao.qr_code == btradeDao.qr_code,OnlinetradesDao.real_amount == btradeDao.amount,OnlinetradesDao.state == 1).all()
    count = len(otradeList)
    if count !=1:
        raise Exception('订单匹配不唯一,匹配到%s个'%(count))
    otradeDao = otradeList[0]
    otradeDao.audit_time = mtime
    otradeDao.state = 2
    otradeDao.bank_order_no = btradeDao.order_no
    otradeDao.match_type = 2
    otradeDao.real_cost_service = otradeDao.cost_service
    otradeDao.real_cost_agent = otradeDao.cost_agent
    otradeDao.bank_amount = otradeDao.amount
    btradeDao.state  = 2
    btradeDao.audit_time = mtime
    merchantDao = db.session.query(MerchantDao).filter(MerchantDao.code == otradeDao.mer_code).first()
    merchantDao.amount = merchantDao.amount + otradeDao.amount - otradeDao.cost_service

    merchant_agent = db.session.query(MerchantDao).filter(MerchantDao.username == merchantDao.parent_name).first()
    merchant_agent.amount = merchant_agent.amount + otradeDao.cost_agent

    db.session.add(otradeDao)
    db.session.add(btradeDao)
    db.session.add(merchantDao)
    db.session.add(merchant_agent)
    try:
        db.session.commit()
        code_manager.finish(otradeDao.qr_code, otradeDao.amount,otradeDao.discount_amount)
        args = {"order_no":otradeDao.order_no,"org_order_no":otradeDao.org_order_no}
        gs = GetsendService(args)
        gs.get_all_data();
    except Exception as e:
        db.session.rollback()
        db.session.remove()
        raise Exception(e)
       
    
    
    
    
