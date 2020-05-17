import ast
import json

from flask import request
from flask_restful import Resource

from app.api_0_1.common import make_response
from app.models import db
from app.models.df_agent_rate_dao import DfAgentRate, SelfAgentRate
from app.models.merchant_dao import MerchantDao, MerchantInfo
from app.service.df_agent_service import Df_Agent
from app.api_0_1.parsers.df_agent_parsers import df_agent_post,df_agent_get,df_agent_put
from app.common import formatDecimal
from app.service.df_merchant_service import get_dfagrate_info


class Df_agent(Resource):

    # 新增代付代理
    def post(self):
        # args = df_agent_post.parse_args()
        args = request.json
        if args['username'] is "":
            return {'success':False, 'errorMsg': '用户名称不能为空'}
        else:
            mem = db.session.query(MerchantDao.username).filter(MerchantDao.username == args['username']).first()
            if mem:
                return {'success': False, 'errorMsg': '用户名称已存在，请重新输入'}

        if args['level'] is "":
            return {'success': False, 'errorMsg': '请选择用户等级'}

        if args['rateInputs'] is "":
            return {'success': False, 'errorMsg': '至少填写一个费率'}

        if args['df_sxf'] is "":
            return {'success': False, 'errorMsg': '请填写手续费'}

        rate = args['rateInputs']

        for data in rate:
            if data['mer_name'] is "":
                return {'success': False, 'errorMsg': '请填写商户名称'}

            if data['gdrate'] is "":
                return {'success': False, 'errorMsg': '请填写固定费率'}

            if data['qjrate'] is "":
                for i in data['qjrate']:
                    if i["ratelower"] is "":
                        return {'success': False, 'errorMsg': '最小费率区间是必填项'}

                return {'success': False, 'errorMsg': '请填写区间费率'}

        date = Df_Agent.insert(self, args)
        return date

    # 查询代付代理
    def get(self):
        args = df_agent_get.parse_args()

        if args['agent_code'] is not None:
            pagination = Df_Agent.searchdetails(self, args)
            result = []
            for item in pagination.items:

                for i in item.rate_amount:
                    if i["ratelower"] is not "":
                        i["ratelower"] = i["ratelower"] / 10000
                    if i['rateupper'] is not "":
                        i["rateupper"] = i["rateupper"] / 10000
                    i.update({"status": False,"addData": False})

                result.append({"username": item.mer_username,
                        'qjrate': item.rate_amount,
                        'gdrate': float('%.3f' % item.rate_prop) * 100,
                       "status": False,
                       "addData": False})

            query = db.session.query(
                MerchantDao.username,
                MerchantDao.secret_key,
                MerchantDao.level,
                MerchantDao.state,
                MerchantDao.wrdraw_amount,
                MerchantInfo.remark,
                MerchantInfo.name,
                MerchantInfo.email,
                MerchantInfo.mobilephone
            )
            query1 = query.outerjoin(MerchantInfo, MerchantInfo.code == MerchantDao.code).filter(MerchantDao.code == args['agent_code']).first()

            username = query1.username
            secret_key = query1.secret_key
            remark = query1.remark
            name = query1.name
            email = query1.email
            mobilephone = query1.mobilephone
            level = query1.level
            state = query1.state
            df_sxf = query1.wrdraw_amount
            critern = set()
            data1 = []
            critern.add(SelfAgentRate.agent_code == args['agent_code'])
            selfrate = get_dfagrate_info(critern)
            if selfrate:
                enen = selfrate.rate_amount
                for i in enen:
                    i.update({"status": False, "addData": False})
                data1 = [{
                    'qjrate': enen,
                    'gdrate': float('%.3f' % selfrate.rate_prop),
                    "username": selfrate.agent_name}]
            return make_response(result, username=username, secret_key=secret_key,
                                 mobilephone=mobilephone, remark=remark, name=name,level=level,state=state,
                                 email=email, df_sxf=float("%.2f" % df_sxf), data1=data1)

        else:
            critern = set()
            critern.add(MerchantDao.type == 4)
            if args['username'] is not None:
                critern.add(MerchantDao.username == args['username'])

            if args['begin_time'] is not None:
                critern.add(MerchantDao.actionTime >= args['begin_time'])

            if args['end_time'] is not None:
                critern.add(MerchantDao.actionTime <= args['end_time'])

            if args['state'] is not None:
                critern.add(MerchantDao.state == args['state'])

            if args['level'] is not None:
                critern.add(MerchantDao.level == args['level'])


            pagination = Df_Agent.searchall(self, critern, args['page'], args['page_size'] )
            result = []
            for item in pagination.items:
                query = db.session.query(DfAgentRate.mer_username).distinct().filter(DfAgentRate.agent_name == item.username).all()
                data = []

                for i in query:
                    data.append(i.mer_username)

                result.append({
                    'code': item.code,
                    'username': item.username,
                    'state': item.state,
                    'levelName': item.level,
                    'amount': float('%.2f' % item.amount),
                    'mer_name': data,
                    'remark':item.remark,
                    'isShow': False
                })

            return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)


    # 修改代付代理信息
    def put(self):
        args = request.json
        data = Df_Agent.update(self, args)
        return data