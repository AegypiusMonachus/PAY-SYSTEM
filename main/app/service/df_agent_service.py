import ast
import json
import time

from app.api_0_1.common import make_response
from app.api_0_1.utils import DEFAULT_MEMBER_PASSWORD
from app.models import db, paginate
from app.models.df_agent_rate_dao import DfAgentRate, SelfAgentRate
from app.models.level_dao import LevelDao
from app.models.merchant_dao import MerchantDao, MerchantInfo
from app.service.serviceutils.utils import encrypt_md5, rando, merRange
from flask import current_app

class Df_Agent():

    # 新增代付代理
    def insert(self, args):
        try:
            df_agent = MerchantDao()
            df_agent.code = merRange()
            df_agent.username = args['username']
            df_agent.level = args['level']
            first = encrypt_md5(DEFAULT_MEMBER_PASSWORD)
            salt = rando()
            df_agent.salt = salt
            df_agent.password = encrypt_md5(first + salt)
            df_agent.type = 4
            df_agent.secret_key = encrypt_md5(df_agent.code)
            df_agent.amount = 0
            df_agent.real_money = 0
            df_agent.default_agents = 0
            df_agent.state = 1
            df_agent.actionTime = int(time.time())
            df_agent.wrdraw_amount = args['df_sxf']
            db.session.add(df_agent)

            df_agentinfo = MerchantInfo()
            if args['mobilephone'] is not None:
                df_agentinfo.mobilephone = args['mobilephone']

            if args['email'] is not None:
                df_agentinfo.email = args['email']

            if args['name'] is not None:
                df_agentinfo.name = args['name']

            if args['remark'] is not None:
                df_agentinfo.remark = args['remark']

            df_agentinfo.code = df_agent.code

            username = None
            rate = args['rateInputs']
            try:
                for data in rate:
                    username = data['mer_name']
                    rate1 = data['gdrate'] / 100
                    list1 = data['qjrate']
                    for i in list1:
                        if i["ratelower"] is not "":
                            i["ratelower"] = i["ratelower"] * 10000
                        if i['rateupper'] is not "":
                            i["rateupper"] = i["rateupper"] * 10000
                    mer = db.session.query(MerchantDao).filter(MerchantDao.username == username, MerchantDao.type == 3).first()
                    if mer:
                        df_agrate = DfAgentRate()
                        df_agrate.agent_code = df_agent.code
                        df_agrate.mer_code = mer.code
                        df_agrate.agent_name = df_agent.username
                        df_agrate.mer_username = mer.username
                        df_agrate.rate_amount = list1
                        df_agrate.rate_prop = rate1
                        db.session.add(df_agrate)
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.exception(e)
                return ("错误信息：不存在%s这个商户" % username)

            rate = args['rateInputs2']
            try:
                for data in rate:
                    if data['gdrate'] is "":
                        data['gdrate'] = 0
                        self_agrate = SelfAgentRate()
                        self_agrate.agent_code = df_agent.code
                        self_agrate.agent_name = df_agent.username
                        self_agrate.rate_amount = data['qjrate']
                        self_agrate.rate_prop = data['gdrate']
                        db.session.add(self_agrate)
                    else:
                        self_agrate = SelfAgentRate()
                        self_agrate.agent_code = df_agent.code
                        self_agrate.agent_name = df_agent.username
                        self_agrate.rate_amount = data['qjrate']
                        self_agrate.rate_prop = data['gdrate']
                        db.session.add(self_agrate)
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.exception(e)
                
            db.session.add(df_agentinfo)
            db.session.commit()
        except:
            current_app.logger.error(e)
            current_app.logger.exception(e)
            db.session.rollback()
            db.session.remove()
            return {'success': False, 'errorMsg': '添加失败'}
        return {'success': True}

    # 查询代付代理详情
    def searchdetails(self,args):
        query = db.session.query(
            DfAgentRate.mer_username,
            DfAgentRate.rate_amount,
            DfAgentRate.rate_prop,

        ).filter(MerchantDao.code == args['agent_code'], DfAgentRate.agent_code == args['agent_code'])

        pagination = paginate(query)
        return pagination

    # 代付代理列表
    def searchall(self, critern=None, page=None, page_size=None):
        query = db.session.query(
            MerchantDao.code,
            MerchantDao.username,
            MerchantDao.state,
            MerchantDao.amount,
            MerchantInfo.remark,
            LevelDao.name.label('level')).order_by(MerchantDao.actionTime.desc())
        query1 = query.outerjoin(LevelDao, LevelDao.id == MerchantDao.level)
        query2 = query1.outerjoin(MerchantInfo, MerchantInfo.code == MerchantDao.code).filter(*critern)

        pagination = query2.paginate(page, page_size, error_out=False)

        return pagination

    # 更改代付代理信息
    def update(self, args):
        try:

            rate = args['rateInputs']
            mer = db.session.query(MerchantDao).filter(MerchantDao.code == args['agent_code']).first()
            if args['state'] is not None:
                mer.state = args['state']

            if args['level'] is not None:
                mer.level = args['level']

            if args['df_sxf'] is not None:
                mer.wrdraw_amount = args['df_sxf']

            merinfo = db.session.query(MerchantInfo).filter(MerchantInfo.code == args['agent_code']).first()

            if args['email'] is not None:
                merinfo.email = args['email']

            if args['name'] is not None:
                merinfo.name = args['name']

            if args['remark'] is not None:
                merinfo.remark = args['remark']

            if args['mobilephone'] is not None:
                merinfo.mobilephone = args['mobilephone']

            rateinfo = db.session.query(DfAgentRate).filter(DfAgentRate.agent_code == args['agent_code']).delete()
            username=None
            try:
                for data in rate:
                    list1 = data['qjrate']
                    for i in list1:
                        if i["ratelower"] is not "":
                            i["ratelower"] = i["ratelower"] * 10000
                        if i['rateupper'] is not "":
                            i["rateupper"] = i["rateupper"] * 10000

                    username = data['username']
                    mer = db.session.query(MerchantDao).filter(MerchantDao.username == username,
                                                               MerchantDao.type == 3).first()
                    if mer:
                        df_agrate = DfAgentRate()
                        df_agrate.agent_code = args['agent_code']
                        df_agrate.mer_code = mer.code
                        df_agrate.agent_name = args['agent_name']
                        df_agrate.mer_username = mer.username
                        df_agrate.rate_amount = list1
                        df_agrate.rate_prop = data['gdrate'] / 100
                        db.session.add(df_agrate)
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.exception(e)
                return ("错误信息：不存在%s这个商户" % username)

            selfrate = db.session.query(SelfAgentRate).filter(SelfAgentRate.agent_code == args['agent_code']).delete()

            rate2 = args['rateInputs2']
            try:
                for data in rate2:
                    username = data['username']
                    self_agrate = SelfAgentRate()
                    self_agrate.agent_name = username
                    self_agrate.agent_code = args['agent_code']
                    self_agrate.rate_amount = data['qjrate']
                    self_agrate.rate_prop = data['gdrate']
                    db.session.add(self_agrate)
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.exception(e)

            db.session.add(mer)
            db.session.add(merinfo)
            db.session.commit()

        except:
            db.session.rollback()
            db.session.remove()
            return {'success': False, 'errorMsg': '更改失败'}
        return {'success': True}