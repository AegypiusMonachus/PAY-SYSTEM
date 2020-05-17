from flask_restful.reqparse import RequestParser

refulationParsers = RequestParser(trim=True)

refulationParsers.add_argument('stop_service', type=int)
refulationParsers.add_argument('exempt', type=int)
refulationParsers.add_argument('notify_times', type=int)
refulationParsers.add_argument('pay_times', type=int)
refulationParsers.add_argument('pay_url_times', type=int)
refulationParsers.add_argument('perday_income', type=float)
refulationParsers.add_argument('repetition_time', type=int)
refulationParsers.add_argument('large_limit_lower', type=float)
refulationParsers.add_argument('large_limit_upper', type=float)
refulationParsers.add_argument('small_limit_lower', type=float)
refulationParsers.add_argument('small_limit_upper', type=float)
refulationParsers.add_argument('agents', type=str)