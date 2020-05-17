from flask_restful.reqparse import RequestParser


dfpaymentresultparser = RequestParser(trim=True)

dfpaymentresultparser.add_argument('mer_code', type=str)
dfpaymentresultparser.add_argument('order_no', type=str)
dfpaymentresultparser.add_argument('sign', type=str)