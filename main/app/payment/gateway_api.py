from flask import Response
from flask_restful import abort
from app.service.qrcode_service import getQRbyTempCode
from config import Config
import os
import json
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.service.gateway_service import GatewayService
from app.log import paylogger
from decimal import Decimal
from app.common import *
from app.models.onlinetrades_dao import *
'''
用户请求支付接口    
'''
class GatewayAPI(Resource):
    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('mer_code', type=str, required=True,nullable=False)
        parser.add_argument('amount', type=str, required=True,nullable=True)
        parser.add_argument('user_name', type=str)
        parser.add_argument('org_order_no', type=str, required=True,nullable=True)
        parser.add_argument('notify_url', type=str, required=True,nullable=True)
        parser.add_argument('org_order_time', type=int, required=True,nullable=True)
        parser.add_argument('pay_type', type=int, required=True,nullable=True)
        parser.add_argument('remark', type=str)
        parser.add_argument('sign', type=str, required=True,nullable=True)
        args = parser.parse_args()
        paylogger.error("支付消息:%s"%(args))
        if not args['mer_code']:
            return {'success':False,"error_code":9011,"error_msg":"商户编号错误"}
        if not args['amount']:
            return {'success':False,"error_code":9012,"error_msg":"金额错误"}
        if not args['org_order_no']:
            return {'success':False,"error_code":9013,"error_msg":"订单号错误"}
        if not args['notify_url']:
            return {'success':False,"error_code":9014,"error_msg":"通知地址错误"}
        if not args['pay_type']:
            return {'success':False,"error_code":9015,"error_msg":"支付类型错误"}
        if not args['sign']:
            return {'success':False,"error_code":9016,"error_msg":"签名不能为空"}
        try:
            service = GatewayService(args)
            result = service.getGateway()
        except Exception as e:
            paylogger.exception(e)
            paylogger.error("%s用户支付异常:%s"%(args['mer_code'],args))
            return {'success':False,"error_code":9099,"error_msg":"支付异常"}
        if service.success == False:
            return {'success':False,"error_code":service.error_code,"error_msg":service.error_msg}
        return result

'''
临时地址有效期验证    
'''
class VerifyTempCodeAPI(Resource):
    def get(self,tempcode):
        if not tempcode:
            return {'success':False,"error_msg":"临时地址错误"}
        from app.redis.redisConnectionManager import PayRedisManager
        redisImpl = PayRedisManager.get_redisImpl()
        value = redisImpl.get(tempcode)
        if value != None:
            result = json.loads(value)
            return {'success': True, "data": result}
        else:
            return {'success': False, "error_msg": "交易已过期"}


class TempCodeAPI(Resource):
    def get(self,tempcode):
        qr_title = getQRbyTempCode(tempcode)
        try:
            if qr_title:
                file_dir = os.path.abspath(Config.STATIC_FOLDER )
                image_data = open(os.path.join(file_dir, '%s' % qr_title), "rb").read()
                resp = Response(image_data, mimetype="image/png")
                return resp
            else:
                abort(500)
        except Exception as e:
            abort(500)

'''
取消訂單
'''
class CancelOrderApi(Resource):

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('order_no', type=str, required=True, nullable=False)
        args = parser.parse_args()
        paylogger.error("取消订单:%s" % (args))
        if not args['order_no']:
            return {'success': False, "error_msg": "取消订单失败"}
        trade = OnlinetradesDao.select_one_unfinished_by_number(args['order_no'])
        if not OnlinetradesDao.cancel(trade):
            return {'success': False, "error_msg": "取消订单异常"}
        try:
            import requests
            requests.get('http://127.0.0.1:8125/main/payCancel', timeout=2)
        except:
            pass
        return {'success': True, "msg": "取消订单成功"}


'''
取消变成待确认
'''
class Reconfirmed(Resource):

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('amount', type=str, required=True, nullable=True)
        parser.add_argument('order_no', type=str, required=True, nullable=True)
        args = parser.parse_args()

        if not args['amount']:
            return {'success':False, "error_msg":"金额错误"}
        if not args['order_no']:
            return {'success':False, "error_msg":"订单号错误"}

        return True


'''
待确认变成匹配成功
'''
class ReconfirmedSuccessed(Resource):

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('amount', type=str, required=True, nullable=True)
        parser.add_argument('order_no', type=str, required=True, nullable=True)
        args = parser.parse_args()

        if not args['amount']:
            return {'success': False, "error_msg": "金额错误"}
        if not args['order_no']:
            return {'success': False, "error_msg": "订单号错误"}

        return True