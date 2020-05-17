from flask_restful.reqparse import RequestParser


dfamountparser = RequestParser(trim=True)

dfamountparser.add_argument('mer_code', type=str)
dfamountparser.add_argument('org_order_no', type=str)
dfamountparser.add_argument('name', type=str)
dfamountparser.add_argument('account_number', type=str)
dfamountparser.add_argument('amount', type=str)
dfamountparser.add_argument('bankcard', type=str)
dfamountparser.add_argument('notify_url', type=str)
dfamountparser.add_argument('sign', type=str)
dfamountparser.add_argument('action_time', type=int)
