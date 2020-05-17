from app.models import db
from app.models.refulation_dao import RefulationDao
from flask_restful import abort
from app.models.merchant_dao import MerchantDao

def getdate():
    res = db.session.query(
        RefulationDao.id,
        RefulationDao.agents,
        RefulationDao.stop_service.label('stop_service'),
        RefulationDao.exempt.label('exempt'),
        RefulationDao.notify_times.label('notify_times'),
        RefulationDao.pay_times.label('pay_times'),
        RefulationDao.pay_url_times.label('pay_url_times'),
        RefulationDao.perday_income.label('perday_income'),
        RefulationDao.repetition_time.label('repetition_time'),
        RefulationDao.large_limit_lower,
        RefulationDao.large_limit_upper,
        RefulationDao.small_limit_lower,
        RefulationDao.small_limit_upper,

    ).first()
    return res

def insert():
    try:
        m_args = {}
        m_args['id'] = 1
        m_args['stop_service'] = 1
        m_args['exempt'] = 1
        m_args['notify_times'] = 1
        m_args['pay_times'] = 1
        m_args['pay_url_times'] = 1
        m_args['perday_income'] = 1
        m_args['repetition_time'] = 1
        m_args['large_limit_lower'] = 1
        m_args['large_limit_upper'] = 1
        m_args['small_limit_lower'] = 1
        m_args['small_limit_upper'] = 1
        rdao = RefulationDao(**m_args)
        db.session.add(rdao)
        db.session.commit()
        res = db.session.query(
            RefulationDao.id
        ).first()
        return res
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)

def update(m_args):
    try:
        m_parm = {key: m_args[key] for key in m_args if m_args[key] is not None}
        RefulationDao.query.filter(RefulationDao.id == m_args['id']).update(m_parm)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)


def get_default_agent():
    res = db.session.query(MerchantDao.username).filter(MerchantDao.type==2).all()
    return res