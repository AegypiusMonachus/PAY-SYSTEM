from flask_restful import Resource, marshal_with, fields
from ..parsers.onlinetrades_parser import getsendParsers
from app.service.getsend_service import GetsendService






class GetSend(Resource):


    def post(self):
        args = getsendParsers.parse_args(strict=True)
        res = GetsendService(args)
        m_args= res.get_all_data()
        if m_args is not None:
            if m_args['errorCode'] == 403:
                return {
                    'success': False,
                    'errorCode': 403,
                    'errorMsg': '该订单不存在'
                }
            if m_args['errorCode'] == 410:
                return {
                    'success': False,
                    'errorCode': 410,
                    'errorMsg': '请先进行人工匹配在进行补发消息请求'
                }
            if m_args['errorCode'] == 404:
                return {
                    'success': False,
                    'errorCode': 404,
                    'errorMsg': '返回路径错误'
                }



        return {"success":True}