from app.models import db
from ..models.merchant_dao import MerchantDao,MerchantBank,MerchantInfo
from app.models.refulation_dao import RefulationDao
from ..models.level_dao import LevelDao
from app.api_0_1.utils import *
from .serviceutils.utils import encrypt_md5,merRange,rando
from flask_restful import abort
import json,time
from flask.json import jsonify
import ast

def getDate(args=None,page=None,per_page=None):
    q1 = db.session.query(
        MerchantDao.id,
        MerchantDao.code.label('code'),
        MerchantDao.username.label('username'),
        MerchantDao.type.label('type'),
        MerchantDao.parent_code.label('parent_code'),
        MerchantDao.parent_name.label('parent_name'),
        MerchantDao.wrdraw_amount.label('wrdraw_amount'),
        MerchantDao.rate.label('rate'),
        MerchantDao.secret_key.label('secret_key'),
        MerchantDao.amount.label('amount'),
        MerchantDao.level.label('level'),
        MerchantDao.state.label('state'),
        MerchantInfo.mobilephone.label('mobilephone'),
        MerchantInfo.email.label('email'),
        MerchantInfo.name.label('name'),
        MerchantInfo.remark.label('remark'),
        MerchantDao.default_level.label('default_level'),
        LevelDao.name.label('levelname')

    ).order_by(MerchantDao.actionTime.desc())
    if args is not None:
        q1 = q1.filter(*args)

    q1 = q1.outerjoin(MerchantInfo,MerchantInfo.code == MerchantDao.code)
    q1 = q1.outerjoin(LevelDao, LevelDao.id == MerchantDao.level)
    res = q1.paginate(page, per_page, error_out=False)
    return res

def getDataByCode(mer_code):
    dao = db.session.query(MerchantDao).filter(MerchantDao.code==mer_code).first()
    return dao

def getDataRefulationDao(parent_name):
    refulationDao = db.session.query(RefulationDao.pay_times).filter(MerchantDao.agents==parent_name).first()
    return refulationDao

def insertData(args):
    m_chant = {}
    m_info = {}

    code = merRange()
    password = encrypt_md5(DEFAULT_MEMBER_PASSWORD)
    salt = rando()
    password = encrypt_md5(password + salt)
    sel_key = encrypt_md5(code)

    if args['parent_name'] is not None:
        res_parent = db.session.query(
            MerchantDao.id,
            MerchantDao.username,
        ).filter(
            MerchantDao.username == args['parent_name'],
            MerchantDao.type == 2,
            MerchantDao.state == 1
        ).first()
        if res_parent is not None:
            parent_code = res_parent.id,
            parent_name = res_parent.username
        else:
            return {
                'success': False,
                'errorCode': 403,
                'errorMsg': '该代理不存在/已关闭'
            }
    else:
        res_parent = db.session.query(
            RefulationDao.agents,
            MerchantDao.id
        )
        res_parent = res_parent.outerjoin(MerchantDao,MerchantDao.username == RefulationDao.agents)
        res_parent = res_parent.first()
        if res_parent is not None:
            parent_code = res_parent.id,
            parent_name = res_parent.agents
    m_chant['username'] = args['username']
    m_chant['wrdraw_amount'] = args['wrdraw_amount']
    m_chant['password'] = password
    m_chant['secret_key'] = sel_key
    m_chant['type'] = 1
    m_chant['parent_code'] = parent_code
    m_chant['parent_name'] = parent_name
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
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)

def UpdataData(m_args):
    m_chant = {}
    m_info = {}
    try:
        m_chant['parent_code'] = m_args['parent_code']
        m_chant['rate'] = ast.literal_eval(m_args['rate'])
        m_chant['level'] = m_args['level']
        m_chant['wrdraw_amount'] = m_args['wrdraw_amount']
        if 'state' in m_args:
            m_chant['state'] = m_args['state']
        MerchantDao.query.filter(MerchantDao.id == m_args['id']).update(m_chant)
        if m_args['mobilephone'] is not None or m_args['email']  is not None or m_args['name'] is not None or m_args['remark'] is not None:
            print('*************************************************************')
            m_info['mobilephone'] = m_args['mobilephone']
            m_info['email'] = m_args['email']
            m_info['name'] = m_args['name']
            m_info['remark'] = m_args['remark']
            code = m_args.pop('code')
            MerchantInfo.query.filter(MerchantInfo.code == code).update(m_info)
        db.session.commit()
        dao = db.session.query(
                MerchantDao.id,
                MerchantDao.code.label('code'),
                MerchantDao.username.label('username'),
                MerchantDao.type.label('type'),
                MerchantDao.parent_code.label('parent_code'),
                MerchantDao.parent_name.label('parent_name'),
                MerchantDao.rate.label('rate'),
                MerchantDao.secret_key.label('secret_key'),
                MerchantDao.amount.label('amount'),
                MerchantDao.wrdraw_amount.label('wrdraw_amount'),
                MerchantDao.level.label('level'),
                MerchantDao.state.label('state'),
                MerchantInfo.mobilephone.label('mobilephone'),
                MerchantInfo.email.label('email'),
                MerchantInfo.name.label('name'),
                MerchantInfo.remark.label('remark'),
                MerchantDao.default_level.label('default_level'),
                LevelDao.name.label('levelname')

            ).filter(MerchantDao.id == m_args['id'])
        dao = dao.outerjoin(MerchantInfo,MerchantInfo.code == MerchantDao.code)
        dao = dao.outerjoin(LevelDao, LevelDao.id == MerchantDao.level)
        dao = dao.all()
        return dao
    except:
        db.session.rollback()
        db.session.remove()
        abort(500)