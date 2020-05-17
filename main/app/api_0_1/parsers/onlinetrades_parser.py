from flask_restful.reqparse import RequestParser
from ..utils import DEFAULT_PAGE,DEFAULT_PAGE_SIZE

onlinetradesParsers = RequestParser(trim=True)
onlinetradesParsers.add_argument('page', type=int,default = DEFAULT_PAGE)
onlinetradesParsers.add_argument('page_size', type=int,default = DEFAULT_PAGE_SIZE)

onlinetradesParsers.add_argument('mer_code', type=str)
onlinetradesParsers.add_argument('username', type=str)
onlinetradesParsers.add_argument('parents_name', type=str)
onlinetradesParsers.add_argument('bank_id', type=int)
onlinetradesParsers.add_argument('agent_code', type=int)
onlinetradesParsers.add_argument('order_no', type=str)
onlinetradesParsers.add_argument('org_order_no', type=str)
onlinetradesParsers.add_argument('state', type=int)
onlinetradesParsers.add_argument('amount_max', type=float)
onlinetradesParsers.add_argument('amount_min', type=float)
onlinetradesParsers.add_argument('begin_time', type=int)
onlinetradesParsers.add_argument('end_time', type=int)
onlinetradesParsers.add_argument('begin_time_au', type=int)
onlinetradesParsers.add_argument('end_time_au', type=int)
onlinetradesParsers.add_argument('pay_type_name', type=str)


onlinetradesParsers_datil = RequestParser(trim=True)
onlinetradesParsers_datil.add_argument('mer_code', type=str)

#----------------------------------------------------------------------------------------
withdrawParsers = RequestParser(trim=True)
withdrawParsers.add_argument('page', type=int)
withdrawParsers.add_argument('page_size', type=int)

withdrawParsers.add_argument('mer_code', type=str)
withdrawParsers.add_argument('username', type=str)
withdrawParsers.add_argument('bank_id', type=int)
withdrawParsers.add_argument('bank_account', type=int)
withdrawParsers.add_argument('order_no', type=str)
withdrawParsers.add_argument('state', type=int)
withdrawParsers.add_argument('amount_max', type=float)
withdrawParsers.add_argument('amount_min', type=float)
withdrawParsers.add_argument('begin_time', type=int)
withdrawParsers.add_argument('end_time', type=int)
withdrawParsers.add_argument('begin_time_au', type=int)
withdrawParsers.add_argument('end_time_au', type=int)
withdrawParsers.add_argument('account', type=str)


withdrawParserspost = RequestParser(trim=True)

withdrawParserspost.add_argument('mer_code', type=str)
withdrawParserspost.add_argument('bank_id', type=int)
withdrawParserspost.add_argument('account', type=int)
withdrawParserspost.add_argument('name', type=str)
withdrawParserspost.add_argument('amount', type=float)


withdrawParsersput = RequestParser(trim=True)

withdrawParsersput.add_argument('order_no', type=str)
withdrawParsersput.add_argument('state', type=int)

#----------------------------------------------------------------------------------------------------------------


getsendParsers = RequestParser(trim=True)

getsendParsers.add_argument('order_no', type=str)
getsendParsers.add_argument('org_order_no', type=str)