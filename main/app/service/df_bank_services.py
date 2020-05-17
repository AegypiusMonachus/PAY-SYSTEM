from sqlalchemy import func,and_
from app.models import db
from app.models.df_bank_dao import DfBanks,DfBanksAndMer
from app.models.merchant_dao import MerchantDao
from flask_restful import abort


class DfBankService():

    def __init__(self):
        pass

    def get_bank(self,critern):
        q = db.session.query(
            DfBanks.id,
            DfBanks.user_name,
            DfBanks.bank_code,
            DfBanks.bank_number,
            DfBanks.name,
        ).filter(*critern)
        q = q.outerjoin(DfBanksAndMer,DfBanks.id == DfBanksAndMer.df_bank_id)
        q = q.outerjoin(MerchantDao, MerchantDao.code == DfBanksAndMer.mer_code)
        q = q.all()
        return q

    def insert_bank(self,args):
        try:
            m_args = {}
            m_args['bank_id'] = args['bankId']
            m_args['user_name'] = args['username']
            m_args['name'] = args['name']
            m_args['bank_number'] = args['bankNumber']
            m_args['default_bank'] = args['d_bank']
            codes = db.session.query(MerchantDao.code).filter(MerchantDao.username == args['username']).first()
            if codes is not None:
                m_args['mer_code'] = codes.code
            else:
                return {
                        'success':False,
                        'errorCode': 400,
                        'errorMsg': '没有这个商户信息'
                        }
            try:

                dao = DfBanks(**m_args)
                db.session.add(dao)
                db.session.commit()
                try:
                    r_args = {}
                    r_args['mer_code'] = codes.code
                    r_args['df_bank_id'] = dao.id
                    dao_and = DfBanksAndMer(**r_args)
                    db.session.add(dao_and)
                    # print(1/0)
                    db.session.commit()

                except:
                    db.session.rollback()
                    db.session.remove()
                    db.session.delete(dao)
                    db.session.commit()

            except:
                db.session.rollback()
                db.session.remove()

        except:
            db.session.rollback()
            db.session.remove()
            abort(500)