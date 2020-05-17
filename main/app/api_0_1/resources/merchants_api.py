from ..common import make_fields, make_response
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, marshal_with, fields
from ..parsers.merchants_parser import MerChantparser,MerChantparserPost,MerChantparserPut
from ...models.merchant_dao import MerchantDao
from ..utils import *
from app.models import db
from app.service.merchant_service import getDate,insertData,UpdataData
from flask.json import jsonify
import json
from app.common import keep_two_del

class MerchantAPI(Resource):
    def get(self,id=None):
        m_args = MerChantparser.parse_args(strict=True)
        critern = set()
        critern.add(MerchantDao.type == 1)
        if id is not None:
            critern.add(MerchantDao.id == id)
        if m_args['mer_code'] is not None:
            critern.add(MerchantDao.code == m_args['mer_code'])
        if m_args['username'] is not None:
            critern.add(MerchantDao.username == m_args['username'])
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
            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0
            if items.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(items.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                "id": items.id,
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "parent_code": items.parent_code,
                "parent_name": items.parent_name,
                "rate": items.rate,
                "secret_key": items.secret_key,
                "amount": amount,
                "wrdraw_amount": wrdraw_amount,
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
        if m_args['level'] is None:
            return jsonify({
                'success': False,
                'errorCode': 403,
                'errorMsg': '会员等级不能为空'
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
                    'errorMsg': '该代理不存在/已关闭'
                }
        args = getDate(page=m_args['page'],per_page=m_args['page_size'])
        result = []
        for items in args.items:
            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0
            if items.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(items.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                        "id": items.id,
                        "code":items.code,
                        "username":items.username,
                        "type":items.type,
                        "parent_code":items.parent_code,
                        "parent_name": items.parent_name,
                        "rate":items.rate,
                        "secret_key":items.secret_key,
                        "amount":amount,
                        "wrdraw_amount": wrdraw_amount,
                        "level":items.level,
                        "state":items.state,
                        "mobilephone":items.mobilephone,
                        "email":items.email,
                        "name":items.name,
                        "remark":items.remark,
                        "default_level":items.default_level,
                        "isShowRate": False,
                        "levelname": items.levelname
                    })

        return make_response(result,page=args.page, pages=args.pages, total=args.total)



    def put(self,id):
        m_args = MerChantparserPut.parse_args(strict=True)
        m_args['id'] = id
        args = UpdataData(m_args)
        result = []
        for items in args:
            if items.amount is not None:
                amount = float('%.2f' % keep_two_del(items.amount))
            else:
                amount = 0
            if items.wrdraw_amount is not None:
                wrdraw_amount = float('%.2f' % keep_two_del(items.wrdraw_amount))
            else:
                wrdraw_amount = 0
            result.append({
                "id": items.id,
                "code": items.code,
                "username": items.username,
                "type": items.type,
                "parent_code": items.parent_code,
                "parent_name": items.parent_name,
                "rate": items.rate,
                "secret_key": items.secret_key,
                "amount": amount,
                "wrdraw_amount": wrdraw_amount,
                "level": items.level,
                "state": items.state,
                "mobilephone": items.mobilephone,
                "email": items.email,
                "name": items.name,
                "remark": items.remark,
                "default_level": items.default_level,
                "isShowRate": False,
                "levelname": items.levelname
            })

        return make_response(result)
