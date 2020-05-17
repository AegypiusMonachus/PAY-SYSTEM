from app.api_0_1.common import make_response_from_pagination,make_fields
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with,fields
from app.api_0_1.utils import (DEFAULT_PAGE,DEFAULT_PAGE_SIZE)
from app.models.bank_trade_dao import BankTradeDao
from app.models import paginate
from app.models import db
from sqlalchemy import desc

class BanktradesAPI(Resource):
    @marshal_with(make_fields({
        'id': fields.Integer,
        'order_no': fields.String,
        'amount': fields.Float,
        'action_time' : fields.Integer,
        'pay_time' : fields.Integer,
        'qr_code': fields.String,
        'state': fields.Integer,
        'audit_time': fields.Integer,
    }))
    def get(self,id=None):
        parser = RequestParser(trim=True)
        parser.add_argument('amount_lower', type=int)
        parser.add_argument('amount_upper', type=int)
        parser.add_argument('begin_time', type=int)
        parser.add_argument('end_time', type=int)
        parser.add_argument('begin_audit_time', type=int)
        parser.add_argument('end_audit_time', type=int)
        parser.add_argument('qr_code', type=str)
        parser.add_argument('state', type=int)
        parser.add_argument('page', type=int, default=DEFAULT_PAGE)
        parser.add_argument('page_size', type=int, default=DEFAULT_PAGE_SIZE)
        args = parser.parse_args(strict=True)
        critern = set()
        if id is not None:
            critern.add(BankTradeDao.id == id)
        if args['amount_lower'] is not None:
            critern.add(BankTradeDao.amount >= args['amount_lower'])
        if args['amount_upper'] is not None:
            critern.add(BankTradeDao.amount <= args['amount_upper'])
        if args['begin_time'] is not None:
            critern.add(BankTradeDao.pay_time >= args['pay_time'])
        if args['end_time'] is not None:
            critern.add(BankTradeDao.pay_time <= args['pay_time'])
        if args['qr_code'] is not None:
            critern.add(BankTradeDao.qr_code == args['qr_code'])
        if args['state'] is not None:
            critern.add(BankTradeDao.state == args['state'])
        if args['begin_audit_time'] is not None:
            critern.add(BankTradeDao.audit_time >= args['begin_audit_time'])
        if args['end_audit_time'] is not None:
            critern.add(BankTradeDao.audit_time <= args['end_audit_time'])
        query = db.session.query(BankTradeDao).order_by(desc(BankTradeDao.action_time))
        pagination = paginate(query, critern, args['page'], args['page_size'])
        return make_response_from_pagination(pagination)
        
        
        
        
        