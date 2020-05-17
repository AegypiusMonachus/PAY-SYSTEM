from flask_restful.reqparse import RequestParser


dfcashwithdrawalparser = RequestParser(trim=True)

dfcashwithdrawalparser.add_argument('mer_code', type=str)
dfcashwithdrawalparser.add_argument('sign', type=str)
dfcashwithdrawalparser.add_argument('org_order_no', type=str)
dfcashwithdrawalparser.add_argument('name', type=str)
dfcashwithdrawalparser.add_argument('account_number', type=str)
dfcashwithdrawalparser.add_argument('amount', type=str)
dfcashwithdrawalparser.add_argument('bankcard', type=int)
dfcashwithdrawalparser.add_argument('action_time', type=int)



dfgetwithdrawalparser = RequestParser(trim=True)

dfgetwithdrawalparser.add_argument('mer_code', type=str)
dfgetwithdrawalparser.add_argument('org_order_no', type=str)
dfgetwithdrawalparser.add_argument('sign', type=str)