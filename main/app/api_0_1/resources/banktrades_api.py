from ..common import make_response_from_pagination,make_fields,make_response
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with,fields
from ..utils import (DEFAULT_PAGE,DEFAULT_PAGE_SIZE)
from app.models.bank_trade_dao import BankTradeDao
from app.models.transaction_code_dao import Qrcode
from app.service.banktrades_service import get_data
from app.models import paginate
from app.models import db
from sqlalchemy import desc, func
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.bank_trade_dao import BankTradeDao
from app.common import keep_two_del

class BanktradesAPI(Resource):

    def get(self,id=None):
        parser = RequestParser(trim=True)
        parser.add_argument('begin_audit_time', type=int)
        parser.add_argument('end_audit_time', type=int)

        parser.add_argument('order_no', type=str)
        parser.add_argument('state', type=int)
        parser.add_argument('page', type=int,default = DEFAULT_PAGE)
        parser.add_argument('page_size', type=int,default = DEFAULT_PAGE_SIZE)
        parser.add_argument('begin_time_au', type=int)
        parser.add_argument('end_time_au', type=int)
        args = parser.parse_args()
        critern = set()

        if args['state'] is not None:
            critern.add(BankTradeDao.state == args['state'])

        if args['begin_audit_time'] is not None:
            critern.add(BankTradeDao.action_time >= args['begin_audit_time'])

        if args['end_audit_time'] is not None:
            critern.add(BankTradeDao.action_time <= args['end_audit_time'])

        if args['order_no'] is not None:
            critern.add(BankTradeDao.order_no == args['order_no'])

        if args['begin_time_au'] is not None:
            critern.add(BankTradeDao.audit_time >= args['begin_time_au'])

        if args['end_time_au'] is not None:
            critern.add(BankTradeDao.audit_time <= args['end_time_au'])

        res = get_data(critern, args['page'], args['page_size'])
        result = []
        for item in res.items:
            if item.amount is not None:
                amount = float('%.2f' % keep_two_del(item.amount))
            else:
                amount = 0
            result.append({
                'id': item.id,
                'order_no': item.order_no,
                'amount': amount,
                'action_time': item.action_time,
                'pay_time': item.pay_time,
                'qr_code':  item.qr_code,
                'state': item.state,
                'audit_time':  item.audit_time,
            })
        query = db.session.query(func.sum(BankTradeDao.amount).label('sumamount')).filter(*critern).first()
        print(query)
        if query.sumamount is not None:
            total = float('%.2f' % query.sumamount)
        else:
            total = 0
        return make_response(result, page=res.page, pages=res.pages, total=res.total, count=total)
        
        
        
        
        