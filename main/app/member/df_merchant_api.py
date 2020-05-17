from flask import g
from flask_restful import Resource

from app.api_0_1.common import make_response
from app.models.df_agent_rate_dao import DfAgentRate, SelfAgentRate
from app.models.merchant_dao import MerchantDao
from app.service.df_merchant_service import get_dfmer_info, get_dfag_info, get_dfagrate_info


class Get_merinfo(Resource):
    def get(self):
        critern = set()
        if g.current_member:
            username = g.current_member.username
            type = g.current_member.type
            critern.add(MerchantDao.username == username)
            critern.add(MerchantDao.type == type)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        data = get_dfmer_info(critern)
        result = []
        for one in data:
            result.append({
                'id': one.id,
                'code': one.code,
                'username': one.username,
                'type': one.type,
                'secret_key': one.secret_key,
                'amount': float('%.2f' %one.amount),
                'level': one.level,
                'state': one.state,
                'mobilephone': one.mobilephone,
                'email': one.email,
                'name': one.name,
                'remark': one.remark,
                'levelname': one.levelname

            })
        return make_response(result)


class Get_aginfo(Resource):
    def get(self):
        critern = set()
        if g.current_member:
            username = g.current_member.username
            critern.add(DfAgentRate.agent_name == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        data = get_dfag_info(critern)
        result = []
        for one in data:
            rate = one[1]

            for i in rate:
                if ["ratelower"] is not "":
                    i["ratelower"] = i["ratelower"] / 10000

                if i['rateupper'] is not "":
                    i["rateupper"] = i["rateupper"] / 10000
            result.append({
                'mer_name': one.mer_username,
                'qjrate': one.rate_amount,
                'gdrate': float('%.3f' % one.rate_prop) * 100,})
        return make_response(result)

class Get_agrateinfo(Resource):
    def get(self):
        critern = set()
        if g.current_member:
            username = g.current_member.username
            critern.add(SelfAgentRate.agent_name == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        data = get_dfagrate_info(critern)
        print(data)
        print(type(data))
        print(data[0])
        result = []

        result.append({
            'mer_name': data[0],
            'qjrate': data[1],
            'gdrate': float('%.3f' % data[2])})
        return make_response(result)