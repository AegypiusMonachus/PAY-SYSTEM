from ..common import make_fields, make_response
from flask_restful import Resource, marshal_with, fields
from app.service.bank_service import getBank,getMerBank,insertMerBank
from app.api_0_1.parsers.bank_parser import bankParsers,bankParserspost



class Bank(Resource):
    def get(self):
        res = getBank()
        result = []
        for items in res:
            result.append({
                'id':items.id,
                'name':items.name
            })
        return make_response(result)

class MerBank(Resource):
    def get(self):
        m_args = bankParsers.parse_args(strict=True)
        if m_args['username'] is None:
            m_args['username'] = 'zzz123'
        res = getMerBank(m_args)

        result = []
        for items in res:
            result.append({
                'bankid':items.bankNumber,
                'account':items.account,
                'name':items.name,
                'username': items.username
            })
        return make_response(result)

    def post(self):
        m_args = bankParserspost.parse_args(strict=True)
        res = insertMerBank(m_args)
        if res is not None:
            return res
        else:
            return {
                'success':True,
                'errorCode': 200,
                'errorMsg': '新增成功'
                }