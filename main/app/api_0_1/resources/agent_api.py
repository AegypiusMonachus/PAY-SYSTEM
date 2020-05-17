from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.api_0_1.parsers.agents_parser import agentsparser,agentsparserpost,agentsparserput
from app.service.agent_service import getDate,insertData,UpdataData,getNumber
from ..common import make_response
from ...models.merchant_dao import MerchantDao
from ..utils import SECONDS_PER_DAY,DEFAULT_MEMBER_PASSWORD,DEFAULT_MEMBER_FUND_PASSWORD
from app.models import db
from flask.json import jsonify
import json
from app.common import keep_two_del


class Agents(Resource):
    # 代理 - 列表查询
    def get(self, code=None):
        m_args = agentsparser.parse_args(strict=True)
        critern = set()
        critern.add(MerchantDao.type != 1)
        if code is not None:
            critern.add(MerchantDao.code == code)
        if m_args['mer_code'] is not None:
            critern.add(MerchantDao.code == m_args['mer_code'])
        if m_args['username'] is not None:
            critern.add(MerchantDao.username == m_args['username'])
        if m_args['begin_time'] is not None:
            critern.add(MerchantDao.actionTime >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(MerchantDao.actionTime <= m_args['end_time'])
        if m_args['state'] is not None:
            critern.add(MerchantDao.state == m_args['state'])
        
        critern.add(MerchantDao.type == 2)
        res = getDate(critern, m_args['page'], m_args['page_size'])
        result = []
        for items in res.items:
            result.append({
                "id":items.id,
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "rate": items.rate,
                "state": items.state,
                "level": items.level,
                "mobilephone": items.mobilephone,
                "email": items.email,
                "name": items.name,
                "remark": items.remark,
                "default_level": items.default_level,
                "levelname": items.levelname,
                "actionTime":items.actionTime,
                "isShowNum": False,
                "isShowRate":False
            })

        return make_response(result, page=res.page, pages=res.pages, total=res.total)


    # 代理 - 新增
    def post(self):
        m_args = agentsparserpost.parse_args(strict=True)
        if m_args['username'] is None:
            return {'errorMsg': "用户名不能为空"}
        if m_args['rate'] is None:
            return {'errorMsg': "费率不能为空"}

        mem = db.session.query(MerchantDao.username).filter(MerchantDao.username == m_args['username']).first()
        if mem is not None:
            return jsonify({
                'success': False,
                'errorCode': 403,
                'errorMsg': '该商户/代理已存在'
            })

        res = insertData(m_args)
        result = []
        for items in res:
            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0
            if items.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(items.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "parent_code": items.parent_code,
                "rate": items.rate,
                "secret_key": items.secret_key,
                "amount": amount,
                "level": items.level,
                "state": items.state,
                "default_level": items.default_level,
                "wrdraw_amount": wrdraw_amount,
                "isShowRate": False,
                "isShowNum": False,
                "actionTime": items.actionTime
            })

        return make_response(result)

    # 代理-修改
    def put(self,code):
        m_args = agentsparserput.parse_args()
        m_args['code'] = code
        args = UpdataData(m_args)
        result = []
        for items in args:

            if items.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(items.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "wrdraw_amount": wrdraw_amount,
                "parent_code": items.parent_code,
                "rate": items.rate,
                "level": items.level,
                "state": items.state,
                "mobilephone": items.mobilephone,
                "email": items.email,
                "name": items.name,
                "remark": items.remark,
                "default_level": items.default_level,
                "levelname": items.levelname,
                "isShowRate": False,
                "isShowNum": False,
                "actionTime": items.actionTime
            })

        return make_response(result)




    # def delete(self,code):
    #     parser = RequestParser(trim=True)
    #     parser.add_argument('is_delete', type=int)
    #     args = parser.parse_args()
    #
    #     msg = AgentsService.isdelete(self, args, code)
    #     return make_response(msg)

class getNumMerchar(Resource):
    def get(self):
        res = getNumber()
        res = res.cursor._rows
        result = []
        for i in res:
            result.append({
                'username':i[0],
                'number':i[1],
                'sh': i[2]
            })

        return make_response(result)