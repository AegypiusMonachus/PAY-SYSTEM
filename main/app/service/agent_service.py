from app.models import db
from ..models.merchant_dao import MerchantDao,MerchantBank,MerchantInfo
from ..models.level_dao import LevelDao
from app.api_0_1.utils import *
from .serviceutils.utils import encrypt_md5,merRange,rando
from flask_restful import abort
import json,time
from sqlalchemy import func
import ast

def getDate(args=None,page=None,per_page=None):
    q1 = db.session.query(
        MerchantDao.id.label('id'),
        MerchantDao.code.label('code'),
        MerchantDao.username.label('username'),
        MerchantDao.type.label('type'),
        MerchantDao.rate.label('rate'),
        MerchantDao.state.label('state'),
        MerchantDao.level.label('level'),
        MerchantInfo.mobilephone.label('mobilephone'),
        MerchantInfo.email.label('email'),
        MerchantInfo.name.label('name'),
        MerchantInfo.remark.label('remark'),
        MerchantDao.default_level.label('default_level'),
        MerchantDao.actionTime,
        LevelDao.name.label('levelname')
    ).order_by(MerchantDao.actionTime.desc())
    if args is not None:
        q1 = q1.filter(*args)

    q1 = q1.outerjoin(MerchantInfo,MerchantInfo.code == MerchantDao.code)
    q1 = q1.outerjoin(LevelDao, LevelDao.id == MerchantDao.level)
    res = q1.paginate(page, per_page, error_out=False)
    return res


def insertData(args):
    m_chant = {}
    m_info = {}

    code = merRange()
    password = encrypt_md5(DEFAULT_MEMBER_PASSWORD)
    salt = rando()
    password = encrypt_md5(password + salt)
    sel_key = encrypt_md5(code)


    m_chant['username'] = args['username']
    m_chant['wrdraw_amount'] = args['wrdraw_amount']
    m_chant['state'] = args['state']
    m_chant['password'] = password
    m_chant['secret_key'] = sel_key
    m_chant['type'] = 2
    m_chant['rate'] = ast.literal_eval(args['rate'])
    m_chant['level'] = args['level']
    m_chant['code'] = code
    m_chant['salt'] = salt
    m_chant['actionTime'] = int(time.time())

    m_info['mobilephone'] = args['mobilephone']
    m_info['email'] = args['email']
    m_info['name'] = args['name']
    m_info['remark'] = args['remark']
    m_info['code'] = code

    m_bank = {}
    m_bank['code'] = code


    try:
        m_dao = MerchantDao(**m_chant)
        m_infos = MerchantInfo(**m_info)
        db.session.add(m_dao)
        db.session.add(m_infos)
        db.session.commit()
        res = db.session.query(
            MerchantDao.code,
            MerchantDao.username,
            MerchantDao.type,
            MerchantDao.parent_code,
            MerchantDao.rate,
            MerchantDao.secret_key,
            MerchantDao.amount,
            MerchantDao.wrdraw_amount,
            MerchantDao.level,
            MerchantDao.state,
            MerchantDao.actionTime,
            MerchantDao.default_level
        ).filter(MerchantDao.code == code)
        res = res.outerjoin(MerchantInfo, MerchantInfo.code == MerchantDao.code)
        res = res.outerjoin(LevelDao, LevelDao.id == MerchantDao.level)
        res = res.all()
        return res
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)


def UpdataData(m_args):
    m_chant = {}
    m_info = {}
    try:
        m_chant['rate'] = ast.literal_eval(m_args['rate'])
        m_chant['level'] = m_args['level']
        m_chant['wrdraw_amount'] = m_args['wrdraw_amount']
        if 'state' in m_args:
            m_chant['state'] = m_args['state']
        MerchantDao.query.filter(MerchantDao.code == m_args['code']).update(m_chant)
        if m_args['mobilephone'] is not None or m_args['email']  is not None or m_args['name'] is not None or m_args['remark'] is not None:
            m_info['mobilephone'] = m_args['mobilephone']
            m_info['email'] = m_args['email']
            m_info['name'] = m_args['name']
            m_info['remark'] = m_args['remark']
            MerchantInfo.query.filter(MerchantInfo.code == m_args['code']).update(m_info)
        db.session.commit()
        dao = db.session.query(
            MerchantDao.code,
            MerchantDao.username,
            MerchantDao.type,
            MerchantDao.parent_code,
            MerchantDao.rate,
            MerchantDao.level,
            MerchantDao.state,
            MerchantDao.default_level,
            MerchantDao.wrdraw_amount,
            MerchantDao.actionTime,
            MerchantInfo.mobilephone.label('mobilephone'),
            MerchantInfo.email.label('email'),
            MerchantInfo.name.label('name'),
            MerchantInfo.remark.label('remark'),
            LevelDao.name.label('levelname')

            ).filter(MerchantDao.code == m_args['code'])
        dao = dao.outerjoin(MerchantInfo,MerchantInfo.code == MerchantDao.code)
        dao = dao.outerjoin(LevelDao, LevelDao.id == MerchantDao.level)
        dao = dao.all()
        return dao
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)

def getNumber():
    m_sql = '''SELECT aa.parent_name,aa.count,
            (SELECT GROUP_CONCAT(username) FROM tb_merchant WHERE parent_name = aa.parent_name) names
            FROM (
            SELECT parent_name,count(username) as count FROM tb_merchant WHERE type = 1 GROUP BY parent_name ) aa'''
    res = db.session.execute(m_sql)
    return res

