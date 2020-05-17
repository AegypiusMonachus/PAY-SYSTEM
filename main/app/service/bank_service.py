from flask import g

from app.models import db
from ..models.withdraw_dao import BankDao
from app.models.withdraw_dao import WithdrawDao,BankDao
from app.models.merchant_dao import MerchantBank,MerchantInfo,MerchantDao
from flask_restful import abort

def getBank():
    res = db.session.query(
        BankDao
    ).all()
    return res



def getMerBank(m_args):
    if g.current_member:
        res = db.session.query(
            MerchantBank.bankNumber,
            MerchantBank.numbers.label('account'),
            MerchantBank.bankname.label('name'),
            MerchantDao.username
        ).filter(MerchantBank.bankNumber == m_args['bank_id'],MerchantDao.username == g.current_member.username)
        res = res.outerjoin(MerchantDao,MerchantDao.code == MerchantBank.code)
        res = res.all()

        return res
    else:
        return {"success": False, "error_code": 999}
def insertMerBank(m_args):
    username = m_args.pop('username')
    mer_code = db.session.query(MerchantDao.code).filter(MerchantDao.username == username).first()
    if mer_code is None:
        return {
                'success':False,
                'errorCode': 403,
                'errorMsg': '该用户不存在'
                }
    m_args['code'] = mer_code[0]
    mer = db.session.query(MerchantBank.code).filter(MerchantBank.code == m_args['code']).first()
    if mer is not None:
        return {
            'success': False,
            'errorCode': 403,
            'errorMsg': '该用户已经绑定过银行卡，请先解绑'
        }
    try:
        m_dao = MerchantBank(**m_args)
        db.session.add(m_dao)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)