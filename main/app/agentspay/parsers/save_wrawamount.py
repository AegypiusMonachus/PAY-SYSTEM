from flask_restful.reqparse import RequestParser



getwithdrawalparser = RequestParser(trim=True)
getwithdrawalparser.add_argument('username', type=str)
getwithdrawalparser.add_argument('action_begin_time', type=int)
getwithdrawalparser.add_argument('action_end_time', type=int)
getwithdrawalparser.add_argument('audit_begin_time', type=int)
getwithdrawalparser.add_argument('audit_end_time', type=int)
getwithdrawalparser.add_argument('state', type=int)
getwithdrawalparser.add_argument('page', type=int)
getwithdrawalparser.add_argument('page_size', type=int)

savewithdrawalparser = RequestParser(trim=True)


savewithdrawalparser.add_argument('amount', type=str)
savewithdrawalparser.add_argument('mer_code', type=str)
savewithdrawalparser.add_argument('remark', type=str)
savewithdrawalparser.add_argument('password', type=str)

savewithdrawalputparser = RequestParser(trim=True)


savewithdrawalputparser.add_argument('state', type=int)
savewithdrawalputparser.add_argument('order_no', type=str)
savewithdrawalparser.add_argument('mer_code', type=str)

