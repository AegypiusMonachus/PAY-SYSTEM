from flask_restful import Resource
from flask import request
from app.service.bank_notify_service import bankNotify
from app.log import banklogger
from app.common import creat_order_no
import time

'''
银行回调接收接口    
'''
class BankNodifyAPI(Resource):
    def post(self,qrcode):
        args = request.json
        #print(args)
        banklogger.error("机构消息 %s:%s"%(qrcode,args))
        if 'amount' not in args and not args['amount']:
            banklogger.error("机构回调错误 %s:%s"%(id,args))
            return {'success':True}
        if 'order_no' not in args and not args['order_no']:
            args['order_no'] = creat_order_no(1000,0)
            #banklogger.error("机构回调错误 %s:%s"%(id,args))
        if 'pay_time' not in args and not args['pay_time']:
            args['pay_time'] = int(time.time())
            #banklogger.error("机构回调错误 %s:%s"%(qrcode,args))
        bankNotify(qrcode,args)
        return {'success':True}
    


        
        
