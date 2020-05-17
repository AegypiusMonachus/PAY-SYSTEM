import os, ast

from app.auth.common import verify_token
from config import Config
from flask import request, Response, current_app, jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.api_0_1.common import make_response
from app.api_0_1.parsers.qrcode_parser import qrcodeparserpost, qrcodeparserget, qrcodeparserput
from app.common import CreatNewQrcode
from app.models import db
from app.models.level_dao import LevelDao
from app.models.refulation_dao import RefulationDao
from app.models.withdraw_dao import BankDao
from app.models.code import CodeLabel
from app.models.transaction_code_dao import Qrcode
from app.service.qrcode_service import QrcodeService
from app.extensions import code_manager
from app.common import *


# 交易码管理
class QrcodeApi(Resource):
    def post(self):
        args = qrcodeparserpost.parse_args()
        print(args)
        query = db.session.query(
            RefulationDao.small_limit_lower,
            RefulationDao.small_limit_upper,
            RefulationDao.large_limit_lower,
            RefulationDao.large_limit_upper).all()
        section = query[0]
        if args['ori_type'] is not None:
            if args['ori_type'] == 1:

                if args['lower_amount'] < section[0]:
                    return {'success': False, 'errorMsg': '个人类型最小金额不能小于最小金额%f' %section[0]}

                if args['lower_amount'] > section[1]:
                    return {'success': False, 'errorMsg': '个人类型最小金额不能大于最大金额%f' % section[1]}

                if args['upper_amount'] < section[0]:
                    return {'success': False, 'errorMsg': '个人类型最大金额不能小于最小金额%f' %section[0]}

                if args['upper_amount'] > section[1]:
                    return {'success': False, 'errorMsg': '个人类型最大金额不能大于最大金额%f' % section[1]}

            if args['ori_type'] == 2:
                if args['lower_amount'] < section[2]:
                    return {'success': False, 'errorMsg': '公司类型最小金额不能小于最小金额%f' %section[2]}

                if args['lower_amount'] > section[3]:
                    return {'success': False, 'errorMsg': '公司类型最小金额不能大于最大金额%f' % section[3]}

                if args['upper_amount'] < section[2]:
                    return {'success': False, 'errorMsg': '公司类型最大金额不能小于最小金额%f' %section[2]}

                if args['upper_amount'] > section[3]:
                    return {'success': False, 'errorMsg': '公司类型最大金额不能大于最大金额%f' % section[3]}
        else:
            return {'success': False, 'errorMsg': '请选择类型'}

        if args['qr_image'] is None:
            return {'success': False, 'errorMsg': '请上传二维码'}

        if args['name'] is None:
            return {'success': False, 'errorMsg': '请输入名称'}

        if args['bank_id'] is None:
            return {'success': False, 'errorMsg': '请选择银行'}

        if args['bank_account'] == "":
            return {'success': False, 'errorMsg': '请输入银行帐号'}

        if args['receive_member'] == "":
            return {'success': False, 'errorMsg': '请输入收款人'}

        if args['rate'] is None:
            return {'success': False, 'errorMsg': '请选择费率'}

        if args['valid_time'] is None:
            return {'success': False, 'errorMsg': '请输入有效分钟数'}

        labels = args['labels']
        labels = labels.split(',')
        msg = QrcodeService.insert(self, args)
        labels = CodeLabel.select_all_by_names(labels)
        qrcode = Qrcode.select_one_by_name(args['name'])
        res = CodeLabel.append_codes(labels, [qrcode])

        return make_response(msg)


    def get(self):
        args = qrcodeparserget.parse_args()
        if args['state'] is not None or args['selectPayType'] is not None or args['bank_account'] is not None or args['name'] is not None:
            msg = QrcodeService.Criteria_query(self,args)
            return msg
        elif args['code'] is not None:
            msg = QrcodeService.searchdetil(self, args)
            return make_response(msg)
        else:
            msg = QrcodeService.searchall(self, args['page'], args['page_size'])
            return msg


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
        result = []
        '''
        query = db.session.query(BankDao.id,BankDao.name).all()
        for i in query:
            data = {}
            data['bankid'] = i.id
            data['bankname'] = i.name
            result.append(data)
        '''
        result.append({
            'bankid': '2001',
            'banknum': '01',
            'bankname': '工商银行',
        })
        result.append({
            'bankid': '2002',
            'banknum': '03',
            'bankname': '农业银行',
        })
        result.append({
            'bankid': '2003',
            'banknum': '05',
            'bankname': '交通银行',
        })
        result.append({
            'bankid': '2004',
            'banknum': '07',
            'bankname': '建设银行',
        })
        result.append({
            'bankid': '2005',
            'banknum': '09',
            'bankname': '招商银行',
        })
        result.append({
            'bankid': '2006',
            'banknum': '11',
            'bankname': '中国银行',
        })
        result.append({
            'bankid': '2007',
            'banknum': '13',
            'bankname': '中信银行',
        })
        result.append({
            'bankid': '2008',
            'banknum': '15',
            'bankname': '浦发银行',
        })
        result.append({
            'bankid': '2009',
            'banknum': '17',
            'bankname': '广东发展银行',
        })
        result.append({
            'bankid': '2010',
            'banknum': '19',
            'bankname': '华夏银行',
        })
        result.append({
            'bankid': '2011',
            'banknum': '21',
            'bankname': '平安银行',
        })
        result.append({
            'bankid': '2012',
            'banknum': '23',
            'bankname': '民生银行',
        })
        result.append({
            'bankid': '2013',
            'banknum': '01',
            'bankname': '光大银行',
        })
        result.append({
            'bankid': '2014',
            'banknum': '27',
            'bankname': '兴业银行',
        })
        result.append({
            'bankid': '2015',
            'banknum': '29',
            'bankname': '邮政储蓄银行',
        })

        return make_response(result)

#图片上传
class Tupian(Resource):

    def post(self):

        img = request.files.get('uploadFile')
        if img and allowed_file(img.filename):
            path = os.path.abspath(Config.STATIC_FOLDER )
            file_path = path + '/' + img.filename
            img.save(file_path)
            name = img.filename
            new_qrcode = CreatNewQrcode(name)
            new_qrcode_name = new_qrcode.creat_new_qrcode()

            return {'success': True,"qr_image": name,"new_qrcode": new_qrcode_name}
        else:
            return {'success': False, "errorMsg": "上传失败"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF']


from decimal import Decimal
def format(value):
    if isinstance(value, float):
        value = Decimal.from_float(value)
    if isinstance(value, int) or isinstance(value, str):
        value = Decimal(value)
    if not isinstance(value, Decimal):
        raise ValueError
    value = value.quantize(Decimal('1.000'))
    return value

# 手动释放二维码状态
class CancelQrcode(Resource):
    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('code', type=str)
        parser.add_argument('amount', type=float)
        parser.add_argument('discount_amount', type=float)
        args = parser.parse_args(strict=True)

        amount = format(args['amount'])
        discount_amount = format(args['discount_amount'])

        code_manager.cancel(args['code'], amount, discount_amount)
        return {'success': True}


# 获取状态
class GetQrcodeState(Resource):
    def get(self):
        res = code_manager.get_status()
        dict_1 = {}
        dict_2 = {}
        dict_3 = {}
        for k, v in res.items():
            val_rec = None
            val_recd = None
            val_kin = None
            for key,value in v.items():

                if key == 'c':
                    print('ccccccc')
                    print(value)
                    for kk,vv in value.items():
                        list_1 = []
                        for list_0 in vv:
                            list_1.append(float(list_0))
                        dict_1 = {float(kk):list_1}
                if key == 'receivable':
                    if value is None:
                        val_rec = 0
                    else:
                        val_rec = float(value)
                if key == 'received':
                    if value is None:
                        val_recd = 0
                    else:
                        val_recd = float(value)
                if key == 'kind':
                    if value is None:
                        val_kin = 0
                    else:
                        val_kin = float(value)
                dict_2 = {'c': dict_1, 'receivable': val_rec, 'received':val_recd, 'kind':val_kin}
            dict_3 = {k: dict_2}
        return dict_3


# 标签管理
class Signs(Resource):

    def get(self):
        signs = CodeLabel.select_all()
        result = []
        for sign in signs:
            data = {}
            data['id'] = sign.id
            data['name'] = sign.name
            result.append(data)

        return result

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('name', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['name']:
            return {'success':False, "error_msg":"标签名错误"}

        res = CodeLabel.insert_label(args['name'])

        if res:
            return {'success': True, "msg": "标签名创建成功"}
        else:
            return {'success': False, "msg": "标签名创建失败"}

    def delete(self):
        parser = RequestParser(trim=True)
        parser.add_argument('name', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['name']:
            return {'success': False, "error_msg": "标签名错误"}
        sign = db.session.query(CodeLabel).filter(CodeLabel.name == args['name']).first()
        try:
            db.session.delete(sign)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.remove()
            return False
        return True

# 标签二维码管理
class SignsQRcode(Resource):

    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('name', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['name']:
            return {'success': False, "error_msg": "标签名错误"}
        sign = CodeLabel.select_one_by_name(args['name'])
        res = []
        for y in sign.codes:
            res.append(y)
        result = []
        for r in res:
            if r.state != 3:
                bankname = db.session.query(BankDao.name).filter(BankDao.id == r.bank_id).first()
                result.append({
                    'id': r.id,
                    'name': r.names,
                    'bankname': bankname[0],
                    'bank_account': r.bank_account,
                    'receive_member': r.receive_member,
                    'valid_time': r.valid_time,
                    'state': r.state,
                    'levels': r.levels,
                    'code': r.code,
                    'isshowlevel': False
                })
        return make_response(result)

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('labels', type=str, required=True, nullable=False)
        parser.add_argument('codes', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['labels']:
            return {'success': False, "error_msg": "标签名错误"}
        if not args['codes']:
            return {'success': False, "error_msg": "二维码错误"}
        labels = args['labels']
        labels = labels.split(',')
        labels = CodeLabel.select_all_by_names(labels)
        if not labels:
            return {'success': False, "msg": "二维码和标签名绑定失败"}
        qrcode = Qrcode.select_one_by_name(args['codes'])
        if not qrcode:
            return {'success': False, "msg": "二维码和标签名绑定失败"}
        res = CodeLabel.append_codes(labels, [qrcode])

        if res:
            return {'success': True, "msg": "二维码和标签名绑定成功"}
        else:
            return {'success': False, "msg": "二维码和标签名绑定失败"}

    def put(self):
        parser = RequestParser(trim=True)
        parser.add_argument('labels', type=str)
        parser.add_argument('codes', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['codes']:
            return {'success': False, "error_msg": "二维码错误"}
        labels = args['labels']
        labels = labels.split(',')
        labels = CodeLabel.select_all_by_names(labels)
        qrcode = Qrcode.select_one_by_code(args['codes'])
        if not qrcode:
            return {'success': False}
        res = CodeLabel.reset_labels(labels, qrcode)
        if res:
            return {'success': True}
        else:
            return {'success': False}

    def delete(self):
        parser = RequestParser(trim=True)
        parser.add_argument('name', type=str, required=True, nullable=False)
        parser.add_argument('qrcodes', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['name']:
            return {'success': False, "error_msg": "标签错误"}
        if not args['qrcodes']:
            return {'success': False, "error_msg": "二维码错误"}

        args['qrcodes'] = ast.literal_eval(args['qrcodes'])
        sign = CodeLabel.select_one_by_name(args['name'])
        qrcodes = db.session.query(Qrcode).filter(Qrcode.id.in_(args['qrcodes'])).all()
        CodeLabel.remove_codes(sign, qrcodes)

        return True

# 二维码获取标签
class GetQRcodeSign(Resource):

    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('code', type=str, required=True, nullable=False)
        args = parser.parse_args()
        if not args['code']:
            return {'success': False, "error_msg": "二维码错误"}
        code = Qrcode.select_one_by_code(args['code'])
        labels = code.labels.all()
        result = []
        for label in labels:
            result.append(label.name)
        return result

# 批次修改二维码状态
class EditQRcode(Resource):

    def put(self):
        parser = RequestParser(trim=True)
        parser.add_argument('codes', type=str, required=True, nullable=False)
        parser.add_argument('state', type=int, required=True, nullable=False)
        args = parser.parse_args()
        if not args['codes']:
            return {'success': False, "error_msg": "标签名错误"}
        if args['state'] is None:
            return {'success': False, "error_msg": "状态值错误"}

        codes = args['codes']
        codes = codes.split(',')
        sign = Qrcode.select_all_by_codes(codes)
        result = BEQRcode(sign, args['state'])
        if not result:
            return {'success': False, "msg": "批次修改失败"}

        from app.extensions import code_manager
        code_manager.refresh()
        return {'success': True, "msg": "批次修改成功"}

