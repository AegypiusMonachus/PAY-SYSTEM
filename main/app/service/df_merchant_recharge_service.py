from app.models import db
import random,json
import decimal, datetime
from app.models.df_trade_dao import DfTradeRechargeDao
from app.models.merchant_dao import MerchantDao
from app.common import creat_order_no
import time
from flask import current_app


'''
Created on 2019年10月3日

@author: ly
'''
def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def get_df_recharge_bank():
    m_sql = '''select drb.id,drb.bank_id df_bank_id,drb.`name` account_name,drb.account account_no,cb.`name` df_bank_name
                from tb_df_recharge_bank drb ,tb_config_bank cb
                where drb.bank_id = cb.id'''
    statement = db.session.execute(m_sql)
    total = statement.rowcount
    if total == 0:
        return None
    banks = statement.fetchall()
    m_index = random.randint(0,total-1)
    m_data = banks[m_index]
    return json.loads(json.dumps(dict(m_data), ensure_ascii=True, default=alchemyencoder))
    
def insert_df_merchnt_recharge(args):
    mdao = db.session.query(MerchantDao).filter(MerchantDao.username == args['username']).first()
    dao = DfTradeRechargeDao(**args)
    dao.order_no = creat_order_no(102, mdao.id)
    dao.mer_code = mdao.code
    dao.action_time = int(time.time())
    db.session.add(dao)
    try:
        db.session.commit()
        return {'success': True}
    except Exception as e:
        db.session.rollback()
        db.session.remove()
        current_app.logger.error(e)
        current_app.logger.exception(e)
        return {'success': False, 'errorMsg': '新增失败','errorCode': 3002}
    
    