import ast
import time

from app.models import db, paginate
from app.models.refulation_dao import RefulationDao
from app.models.transaction_code_dao import Qrcode
from app.models.withdraw_dao import BankDao
from app.service.serviceutils.utils import merRange
from app.extensions import code_manager
from app.common import *
from app.api_0_1.common import *


class QrcodeService():
    # 新增
    def insert(self,args):
        qrcode = Qrcode()
        qrcode.names = args['name']
        qrcode.code = QRcodeNum(args['bank_num'], args['ori_type'])
        qrcode.remark = args['remark']
        qrcode.qr_image = args['qr_image']
        qrcode.bank_id = args['bank_id']
        qrcode.rate = ast.literal_eval(args['rate'])
        qrcode.receive_member = args['receive_member']
        qrcode.bank_account = args['bank_account']
        qrcode.valid_time = args['valid_time']
        qrcode.phone_number = args['phone_number']
        qrcode.state = 1
        qrcode.create_time = int(time.time())
        qrcode.lower_amount = args['lower_amount']
        qrcode.upper_amount = args['upper_amount']
        qrcode.ori_type = args['ori_type']
        qrcode.new_qrcode = args['new_qrcode']

        if 'levels' in args:
            qrcode.levels = ast.literal_eval(args['levels'])
        # query = db.session.query(
        #         RefulationDao.small_limit_lower,
        #         RefulationDao.small_limit_upper,
        #         RefulationDao.large_limit_lower,
        #         RefulationDao.large_limit_upper).all()
        #
        # section = query[0]
        #
        # if section[0] <= args['lower_amount'] and args['upper_amount'] <= section[1]:
        #     qrcode.type = 2
        # elif section[2] <= args['lower_amount'] and args['upper_amount'] <= section[3]:
        #     qrcode.type = 1
        # else:
        #     qrcode.type = 3
        #

        try:
            db.session.add(qrcode)
            db.session.commit()

            code_manager.refresh()
        except:
            db.session.rollback()
            db.session.remove()
            return {'success': False, 'errorMsg': '新增失败'}
        return {'success': True, 'message': '新增成功'}

    # 条件查询
    def Criteria_query(self,args):
        criterion = set()
        criterion.add(Qrcode.state != 3)
        if args['state'] is not None:
            criterion.add(Qrcode.state == args['state'])
        if args['selectPayType'] is not None:
            criterion.add(Qrcode.ori_type.in_(args['selectPayType'].split(',')))
        if args['name'] is not None:
            criterion.add(Qrcode.names == args['name'])
        if args['bank_account'] is not None:
            criterion.add(Qrcode.bank_account == args['bank_account'])

        query = db.session.query(
            Qrcode.id,
            Qrcode.names,
            Qrcode.bank_id,
            Qrcode.bank_account,
            Qrcode.receive_member,
            Qrcode.valid_time,
            Qrcode.state,
            Qrcode.levels,
            Qrcode.code
            ).order_by(Qrcode.create_time.desc())

        result = []
        pagination = paginate(query, criterion, args['page'], args['page_size'])
        for item in pagination.items:
            if item.state != 3:
                bankname = db.session.query(BankDao.name).filter(BankDao.id == item.bank_id).first()
                result.append({
                    'id': item.id,
                    'name': item.names,
                    'bankname': bankname,
                    'bank_account': item.bank_account,
                    'receive_member': item.receive_member,
                    'valid_time': item.valid_time,
                    'state': item.state,
                    'levels': item.levels,
                    'code': item.code,
                    'isshowlevel': False
                })
        return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)

    # 查询全部
    def searchall(self, page, pageSize):
        criterion = set()
        criterion.add(Qrcode.bank_id == BankDao.id)
        criterion.add(Qrcode.state != 3)
        query = db.session.query(
            Qrcode.id,
            Qrcode.names,
            Qrcode.bank_id,
            Qrcode.bank_account,
            Qrcode.receive_member,
            Qrcode.valid_time,
            Qrcode.state,
            Qrcode.levels,
            Qrcode.code,
            BankDao.name
            ).order_by(Qrcode.create_time.desc())

        result = []
        pagination = paginate(query,criterion, page, pageSize)
        for item in pagination.items:
            result.append({
                'id': item.id,
                'name': item.names,
                'bankname': item.name,
                'bank_account': item.bank_account,
                'receive_member': item.receive_member,
                'valid_time': item.valid_time,
                'state': item.state,
                'levels': item.levels,
                'code': item.code,
                'isshowlevel': False
            })
        return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)


#     查询详情
    def searchdetil(self, args):
        criterion = set()
        criterion.add(Qrcode.code == args['code'])
        criterion.add(Qrcode.state != 3)
        query = db.session.query(
            Qrcode.id,
            Qrcode.names,
            Qrcode.bank_id,
            Qrcode.new_qrcode,
            Qrcode.receive_member,
            Qrcode.valid_time,
            Qrcode.state,
            Qrcode.levels,
            Qrcode.code,
            Qrcode.bank_account
        ).order_by(Qrcode.create_time.desc())

        result = []
        pagination = paginate(query, criterion)
        for item in pagination.items:
            bankname = db.session.query(BankDao.name).filter(BankDao.id == item.bank_id).first()
            result.append({
                'id': item.id,
                'name': item.names,
                'receive_member': item.receive_member,
                'valid_time': item.valid_time,
                'state': item.state,
                'levels': item.levels,
                'new_qrcode': item.new_qrcode,
                'code': item.code,
                'bank_account': item.bank_account,
                'bankname': bankname[0],

            })
        return result

    def update(self,args):
        qrcode = db.session.query(Qrcode).filter(Qrcode.code == args['code']).first()
        if args['name'] is not None:
            qrcode.names = args['name']

        if args['qr_image'] is not None:
            qrcode.qr_image = args['qr_image']

        if args['new_qrcode'] is not None:
            qrcode.new_qrcode = args['new_qrcode']

        if args['valid_time'] is not None:
            qrcode.valid_time = args['valid_time']

        if args['levels'] is not None:
            qrcode.levels = ast.literal_eval(args['levels'])

        flag = False
        if args['state'] is not None:
            qrcode.state = args['state']
            flag = True

        if args['receive_member'] is not None:
            qrcode.receive_member = args['receive_member']

        try:
            db.session.add(qrcode)
            db.session.commit()

            if flag:
                code_manager.refresh()
        except:
            db.session.rollback()
            db.session.remove()
            return {'success': False, 'errorMsg': '修改失败'}

        return {'success': True, 'message': '修改成功'}

def getQRbyTempCode(tempcode):
    msql = '''select new_qrcode from tb_qrcode where code = 
            (select qr_code from tb_onlinetrade where order_no = 
            (select order_no from tb_onlinetrade_expansion where temp_code = '%s'))'''%(tempcode)
    result = db.session.execute(msql)
    qr = result.scalar()
    return qr
        

