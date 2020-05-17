from app.api_0_1.common import make_fields, make_response
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
from app.api_0_1.parsers.merchants_parser import MerChantparser,MerChantparserPost,MerChantparserPut
from app.models.merchant_dao import MerchantDao, MerchantInfo
from app.api_0_1.utils import *
from app.models import db
from app.service.merchant_service import getDate,insertData,UpdataData
from flask.json import jsonify
import json
from flask import g

from app.service.serviceutils.utils import encrypt_md5, rando


class MerchantAPI(Resource):
    def get(self,id=None):
        m_args = MerChantparser.parse_args(strict=True)
        critern = set()
        critern.add(MerchantDao.type == 1)
        if g.current_member:
            username = g.current_member.username
            critern.add(MerchantDao.username == username)
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        if id is not None:
            critern.add(MerchantDao.id == id)
        if m_args['mer_code'] is not None:
            critern.add(MerchantDao.code == m_args['mer_code'])
        if m_args['begin_time'] is not None:
            critern.add(MerchantDao.actionTime >= m_args['begin_time'])
        if m_args['end_time'] is not None:
            critern.add(MerchantDao.actionTime <= m_args['end_time'])
        if m_args['begin_wrdraw_amount'] is not None:
            critern.add(MerchantDao.wrdraw_amount >= m_args['begin_wrdraw_amount'])
        if m_args['end_wrdraw_amount'] is not None:
            critern.add(MerchantDao.wrdraw_amount <= m_args['end_wrdraw_amount'])
        if m_args['parent_code'] is not None:
            critern.add(MerchantDao.parent_code == m_args['parent_code'])
        if m_args['parent_name'] is not None:
            critern.add(MerchantDao.parent_name == m_args['parent_name'])
        if m_args['state'] is not None:
            critern.add(MerchantDao.state == m_args['state'])
        if m_args['level'] is not None:
            critern.add(MerchantDao.level == m_args['level'])

        res = getDate(critern,m_args['page'],m_args['page_size'])
        result = []
        for items in res.items:
            result.append({
                "id": items.id,
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "parent_code": items.parent_code,
                "parent_name": items.parent_name,
                "rate": items.rate,
                "secret_key": items.secret_key,
                "amount": items.amount,
                "wrdraw_amount": items.wrdraw_amount,
                "level": items.level,
                "state": items.state,
                "mobilephone": items.mobilephone,
                "email": items.email,
                "name": items.name,
                "remark": items.remark,
                "default_level": items.default_level,
                "isShowRate": False,
                "levelname":items.levelname
            })

        return make_response(result, page=res.page, pages=res.pages, total=res.total)


    def post(self):
        m_args = MerChantparserPost.parse_args(strict=True)
        if m_args['username'] is None:
            return jsonify({
                'success': False,
                'errorCode': 403,
                'errorMsg': '用户名不能为空'
            })
        mem = db.session.query(MerchantDao.username).filter(MerchantDao.username == m_args['username']).first()
        if mem is not None:
            return jsonify({
                'success': False,
                'errorCode': 403,
                'errorMsg': '该商户/代理已存在'
            })

        res = insertData(m_args)
        if res:
            if res['success'] is False:
                return {
                    'success': False,
                    'errorCode': 403,
                    'errorMsg': '该代理不存在'
                }
        args = getDate(page=m_args['page'],per_page=m_args['page_size'])
        result = []
        for items in args.items:
            result.append({
                        "id": items.id,
                        "code":items.code,
                        "username":items.username,
                        "type":items.type,
                        "parent_code":items.parent_code,
                        "rate":items.rate,
                        "secret_key":items.secret_key,
                        "amount":items.amount,
                        "level":items.level,
                        "state":items.state,
                        "mobilephone":items.mobilephone,
                        "email":items.email,
                        "name":items.name,
                        "remark":items.remark,
                        "default_level":items.default_level,
                        "levelname": items.levelname
                    })

        return make_response(result,page=args.page, pages=args.pages, total=args.total)


    def put(self,id):
        m_args = MerChantparserPut.parse_args(strict=True)
        m_args['id'] = id
        args = UpdataData(m_args)
        result = []
        for items in args:
            result.append({
                "id": items.id,
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "parent_code": items.parent_code,
                "rate": items.rate,
                "secret_key": items.secret_key,
                "amount": items.amount,
                "level": items.level,
                "state": items.state,
                "mobilephone": items.mobilephone,
                "email": items.email,
                "name": items.name,
                "remark": items.remark,
                "default_level": items.default_level,
                "levelname": items.levelname
            })

        return make_response(result)


class MerchantInfoAPI(Resource):
    def get(self):
        if g.current_member:
            username = g.current_member.username
        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请登录'
            }
        query_res = db.session.query(
            MerchantDao.id,
            MerchantDao.code,
            MerchantDao.username,
            MerchantDao.secret_key,
            MerchantDao.amount,
            MerchantDao.rate
        ).filter(MerchantDao.username == username).first()
        if query_res is not None:
            query_res_info = db.session.query(MerchantInfo).filter(MerchantInfo.code==query_res.code).first()

            result = []
            result.append({
                "id": query_res.id,
                "code":query_res.code,
                "username":query_res.username,
                "secret_key":query_res.secret_key,
                "amount":float(query_res.amount),
                "rate":query_res.rate,
                "name":query_res_info.name,
                "mobilephone":query_res_info.mobilephone,
                "email":query_res_info.email,
                "remark":query_res_info.remark

            })
            return result

class Changepassworld(Resource):
    def put(self):
        parser  = RequestParser(trim=True)
        parser.add_argument('oldps', type=str)
        parser.add_argument('newps', type=str)
        parser.add_argument('Contrast', type=str)
        args = parser.parse_args(strict=True)


        if args['oldps'] is None:
            return {'success': False,'errorMsg': '请输入旧密码'}

        if args['newps'] is None:
            return {'success': False, 'errorMsg': '请输入新密码'}

        if args['Contrast'] is None:
            return {'success': False, 'errorMsg': '请再次输入新密码'}

        if args['newps'] != args['Contrast']:
            return {'success': False, 'errorMsg': '新密码两次输入不一致'}

        if g.current_member:
            username = g.current_member.username

            merchant = db.session.query(MerchantDao).filter(MerchantDao.username == username).first()
            salt = str(merchant.salt)

            last = encrypt_md5(args['oldps'] + salt)
            if last == merchant.password:
                salt = rando()
                password = encrypt_md5(args['Contrast'] + salt)

                merchant.salt = salt
                merchant.password = password

                db.session.add(merchant)
                db.session.commit()
                return {'success': True, 'message': '密码已更改'}

            else:
                return {'success': False, 'errorMsg': '旧密码输入不正确'}

        else:
            return {
                'success': False,
                'errorCode': 402,
                'errorMsg': '请重新登录'
            }
