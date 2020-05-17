import time

from app.api_0_1.utils import DEFAULT_MEMBER_PASSWORD
from app.models import db
from app.models.df_agent_rate_dao import DfAgentRate, SelfAgentRate
from app.models.df_bank_dao import DfBanksAndMer
from app.models.level_dao import LevelDao
from app.models.merchant_dao import MerchantDao, MerchantInfo
from app.models.refulation_dao import RefulationDao
from app.service.serviceutils.utils import merRange, encrypt_md5, rando


class Df_Merchant():

    # 新增代付商户
    def insert(self, args):
        try:
            df_merchant = MerchantDao()
            df_merchant.code = merRange()
            df_merchant.username = args['username']
            first = encrypt_md5(DEFAULT_MEMBER_PASSWORD)
            salt = rando()
            df_merchant.salt = salt
            df_merchant.password = encrypt_md5(first + salt)
            df_merchant.type = 3 #代付商户type为 3
            df_merchant.secret_key = encrypt_md5(df_merchant.code)
            df_merchant.amount = 0
            df_merchant.real_money = 0
            df_merchant.default_agents = 0
            df_merchant.state = 1
            df_merchant.level = args['level']
            df_merchant.actionTime = int(time.time())
            db.session.add(df_merchant)

            df_merchantinfo = MerchantInfo()
            if args['mobilephone'] is not None:
                df_merchantinfo.mobilephone = args['mobilephone']
            if args['email'] is not None:
                df_merchantinfo.email = args['email']
            if args['name'] is not None:
                df_merchantinfo.name = args['name']
            if args['remark'] is not None:
                df_merchantinfo.remark = args['remark']
            df_merchantinfo.code = df_merchant.code
            db.session.add(df_merchantinfo)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.remove()
            return {'success': False, 'errorMsg': '添加失败'}
        return {'success': True}

    # 查询代付商户详情
    def searchdetails(self,args):
        query = db.session.query(
            MerchantDao.username,
            MerchantDao.state,
            MerchantDao.amount,
            MerchantDao.secret_key,
            MerchantInfo.mobilephone,
            MerchantInfo.name,
            MerchantInfo.email,
            MerchantInfo.remark,
            MerchantDao.level,
            )
        query2 = query.outerjoin(MerchantInfo, MerchantInfo.code == MerchantDao.code).filter(MerchantDao.code == args['mer_code']).first()
        result = []
        result.append({
            'username': query2.username,
            'state': query2.state,
            'secret_key': query2.secret_key,
            'mobilephone': query2.mobilephone,
            'name': query2.name,
            'email': query2.email,
            'remark': query2.remark,
            'level': query2.level,
            'amount':float('%.2f' %query2.amount)
        })
        return result

    # 查询代付商户列表
    def searchall(self, critern=None, page=None, page_size =None):
        query = db.session.query(
            MerchantDao.code,
            MerchantDao.username,
            MerchantDao.state,
            MerchantDao.amount,
            MerchantInfo.mobilephone,
            MerchantInfo.email,
            MerchantInfo.name,
            MerchantInfo.remark,
            LevelDao.name.label('level')).order_by(MerchantDao.actionTime.desc())
        query1 = query.outerjoin(MerchantInfo, MerchantInfo.code == MerchantDao.code)
        query2 = query1.outerjoin(LevelDao, LevelDao.id == MerchantDao.level).filter(*critern)
        pagination = query2.paginate(page, page_size, error_out=False)

        return pagination


    # 更改代付商户信息
    def update(self, args):
        try:
            mer = db.session.query(MerchantDao).filter(MerchantDao.code == args['mer_code']).first()
            if args['state'] is not None:
                mer.state = args['state']

            if args['level'] is not None:
                mer.level = args['level']

            merinfo = db.session.query(MerchantInfo).filter(MerchantInfo.code == args['mer_code']).first()
            if args['email'] is not None:
                merinfo.email = args['email']

            if args['name'] is not None:
                merinfo.name = args['name']

            if args['remark'] is not None:
                merinfo.remark = args['remark']

            if args['mobilephone'] is not None:
                merinfo.mobilephone = args['mobilephone']

            db.session.add(mer)
            db.session.add(merinfo)
            db.session.commit()

        except:
            db.session.rollback()
            db.session.remove()
            return {'success': False, 'errorMsg': '更改失败'}
        return {'success': True}


def get_dfmer_info(args=None):
    q1 = db.session.query(
        MerchantDao.id,
        MerchantDao.code.label('code'),
        MerchantDao.username.label('username'),
        MerchantDao.type.label('type'),
        MerchantDao.secret_key.label('secret_key'),
        MerchantDao.amount.label('amount'),
        MerchantDao.level.label('level'),
        MerchantDao.state.label('state'),
        MerchantInfo.mobilephone.label('mobilephone'),
        MerchantInfo.email.label('email'),
        MerchantInfo.name.label('name'),
        MerchantInfo.remark.label('remark'),
        LevelDao.name.label('levelname'))


    q1 = q1.outerjoin(MerchantInfo,MerchantInfo.code == MerchantDao.code)
    q1 = q1.outerjoin(LevelDao, LevelDao.id == MerchantDao.level).filter(*args).all()

    return q1


def get_dfag_info(args=None):
    data = db.session.query(DfAgentRate.mer_username,
                          DfAgentRate.rate_amount,
                          DfAgentRate.rate_prop).filter(*args).all()
    return data


def get_dfagrate_info(args=None):
    data = db.session.query(SelfAgentRate.agent_name,
                            SelfAgentRate.rate_amount,
                            SelfAgentRate.rate_prop).filter(*args).first()
    return data