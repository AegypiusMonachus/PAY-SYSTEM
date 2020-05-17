from flask_restful import Resource
from sqlalchemy import and_, func

from app.api_0_1.common import make_response
from app.models import db
from app.models.df_agent_rate_dao import DfAgentRate
from app.models.df_bank_dao import DfBanks
from app.models.merchant_dao import MerchantDao
from app.service.df_merchant_service import Df_Merchant
from app.api_0_1.parsers.df_merchant_parsers import df_merchant_post,df_merchant_get,df_merchant_put


class Df_merchant(Resource):

    # 新增代付商户
    def post(self):
        args = df_merchant_post.parse_args()

        if args['username'] is None:
            return {'success':False, 'errorMsg': '商户名称不能为空'}
        else:
            mem = db.session.query(MerchantDao.username).filter(MerchantDao.username == args['username']).first()
            if mem:
                return {'success': False, 'errorMsg': '商户名称已存在，请重新输入'}

        if args['level'] is None:
            return {'success': False, 'errorMsg': '请选择商户等级'}

        date = Df_Merchant.insert(self, args)
        return date

    # 查询代付商户
    def get(self):
        args = df_merchant_get.parse_args()

        if args['mer_code'] is not None:
            data = Df_Merchant.searchdetails(self, args)
            return make_response(data)

        else:
            critern = set()
            critern.add(MerchantDao.type == 3)
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

            pagination = Df_Merchant.searchall(self, critern, args['page'], args['page_size'])
            result = []
            for item in pagination.items:
                count = db.session.query(DfAgentRate.agent_code).distinct().filter(and_(DfAgentRate.mer_code == item.code,
                                                                               MerchantDao.type == 4)).count()
                query = db.session.query(DfAgentRate.agent_name).distinct().filter(DfAgentRate.mer_code == item.code,
                                                                                   MerchantDao.type == 4).all()
                data = []
                for i in query:

                    data.append(i.agent_name)

                result.append({
                    'code': item.code,
                    'username': item.username,
                    'state': item.state,
                    'levelName': item.level,
                    'email': item.email,
                    'remark': item.remark,
                    'amount': float('%.2f' %item.amount),
                    'name': item.name,
                    'mobilephone': item.mobilephone,
                    "agentcount": count,
                    'isShow': False,
                    'agentname':data

                })

            return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)

    # 修改商户信息
    def put(self):
        args = df_merchant_put.parse_args()
        data = Df_Merchant.update(self, args)
        return data


# 查询商户的代理
class Aboutagent(Resource):
    def get(self,mer_code):
        query = db.session.query(DfAgentRate.agent_name).distinct().filter(DfAgentRate.mer_code == mer_code,
                                                                                MerchantDao.type == 4).all()
        result =[]
        for i in query:
            result.append(i.agent_name)

        return result

