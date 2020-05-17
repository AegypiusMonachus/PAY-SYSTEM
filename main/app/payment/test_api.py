from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
import hashlib


class TestApi(Resource):
    def get(self):
        test_parser = RequestParser(trim=True)

        test_parser.add_argument('order_no', type=str)
        test_parser.add_argument('mer_code', type=str)
        test_parser.add_argument('org_order_no', type=str)
        test_parser.add_argument('amount', type=float)
        test_parser.add_argument('real_amount', type=float)
        test_parser.add_argument('pay_type', type=int)
        test_parser.add_argument('sign', type=str)
        test_parser.add_argument('audit_time', type=int)
        test_parser.add_argument('state', type=int)
        test_parsers = test_parser.parse_args(strict=True)
        m_args = {}
        m_args['order_no'] = test_parsers['order_no']
        m_args['audit_time'] = test_parsers['audit_time']
        m_args['state'] = test_parsers['state']
        m_str = 'amount=%s&audit_time=%s&mer_code=%s&order_no=%s&org_order_no=%s&pay_type=%s&real_amount=%s&state=%s&'%(
            test_parsers['amount'],test_parsers['audit_time'],test_parsers['mer_code'],
            test_parsers['order_no'], test_parsers['org_order_no'], test_parsers['pay_type'],
            test_parsers['real_amount'], test_parsers['state']
        )

        md = hashlib.md5()
        md.update((m_str).encode())
        m_sign = md.hexdigest()
        print('接收到加密后的数据:%s'%m_sign)
        if m_sign == test_parsers['sign']:
            return {'success':True}


