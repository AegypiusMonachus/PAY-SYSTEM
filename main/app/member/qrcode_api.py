from flask_restful import Resource

from app.api_0_1.common import make_response
from app.api_0_1.parsers.qrcode_parser import qrcodeparserpost, qrcodeparserget, qrcodeparserput
from app.models import db
from app.models.level_dao import LevelDao
from app.models.withdraw_dao import BankDao
from app.service.qrcode_service import QrcodeService

# 交易码管理
class QrcodeApi(Resource):
    def post(self):
        args = qrcodeparserpost.parse_args()

        if args['qr_image'] is None:
            return {'errorMsg': '请上传二维码'}

        if args['name'] is None:
            return {'errorMsg': '请输入名称'}

        if args['bank_id'] is None:
            return {'errorMsg': '请选择银行'}

        if args['bank_account'] is None:
            return {'errorMsg': '请输入银行帐号'}

        if args['phone_number'] is None:
            return {'errorMsg': '请输入手机号'}

        if args['rate'] is None:
            return {'errorMsg': '请选择费率'}

        if args['valid_time'] is None:
            return {'errorMsg': '请输入有效分钟数'}

        msg = QrcodeService.insert(self, args)
        return make_response(msg)


    def get(self):
        args = qrcodeparserget.parse_args()
        if args['state'] is not None:
            msg = QrcodeService.Criteria_query(self,args)
            return make_response(msg)
        elif args['code'] is not None:
            msg = QrcodeService.searchdetil(self, args)
            return make_response(msg)
        else:
            msg = QrcodeService.searchall(self)
            return make_response(msg)


    def put(self):
        args = qrcodeparserput.parse_args()
        msg = QrcodeService.update(self,args)
        return msg


# 获取等级
class Get_level(Resource):
    def get(self):
        query = db.session.query(LevelDao.name,LevelDao.id).all()
        result = []
        for i in query:
            data = {}
            data['level'] = i.id
            data['levelname'] = i.name
            result.append(data)

        return make_response(result)

# 获取银行
class Get_bank_name(Resource):
    def get(self):
        query = db.session.query(BankDao.id,BankDao.name).all()
        result = []
        for i in query:
            data = {}
            data['bankid'] = i.id
            data['bankname'] = i.name
            result.append(data)

        return make_response(result)