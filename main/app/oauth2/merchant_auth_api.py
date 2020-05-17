import hashlib

from flask import redirect,request
from flask_restful import Resource
import random,time,json
from flask_restful.reqparse import RequestParser
import uuid

from app.api_0_1.utils import DEFAULT_MEMBER_PASSWORD
from app.models import db
from app.models.merchant_dao import MerchantDao
from app.redis.redisConnectionManager import AuthRedisManager
from app.service.serviceutils.utils import encrypt_md5


class MerchantAuthAPI(Resource):
    def get(self):
        print("------------------------------------")
#         parser = RequestParser(trim=True)
#         parser.add_argument('username', type=str)
#         parser.add_argument('password', type=str)
#         parser.add_argument('redirect_uri', type=str)
#         parser.add_argument('code', type=str)
#         parser.add_argument('client_id', type=str)
#         parser.add_argument('grant_type', type=int)
#         args = parser.parse_args(strict=True)
        args = request.args.to_dict()
        #这里不对redirect_uri的合法性进行验证，因为全是内网的路径
        if self.verifyRedirectURL("") == False:
            return {'success': False}
        if 'username' in args and 'password' in args:
            #验证用户名密码
            grant_type = self.verifyMerchant(args['username'], args['password'])
            if  grant_type == -1:
                return {'success': False, 'errorMsg': 'not find user'}
            uri = args['redirect_uri']+'?code=%s&grant_type=%s&client_id=%s' %(self.gen_auth_code(),grant_type,args['username'])
            return redirect(uri)
        if 'code' in args:
            if self.verifyCode(args['code']) == False:
                return {'success': False}
            self.gen_token(args)
            return {'success': True,'token':args['access_token'],'grant_type':args['grant_type']}
    
    def gen_token(self,args):
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        args['access_token'] = suid
        args['refresh_token'] = suid
        args["expires_in"] = int(time.time()) + 2 * 3600
        args["scope"] = "/merchant/0.1"
        redisImpl = AuthRedisManager.get_redisImpl()
        redisImpl.set(suid, json.dumps(args), 2 * 3600)
        return args
        
    def gen_auth_code(self):
        code = random.randint(1,1000)
        return code
        
    def verifyCode(self,code):
        return True
    
    def verifyMerchant(self,username, password):
        merchant = db.session.query(MerchantDao.username, MerchantDao.password, MerchantDao.salt,MerchantDao.type).filter(MerchantDao.username == username).first()
        if not merchant:
            return -1
        else:
            salt = str(merchant.salt)
#             first = encrypt_md5(password)
            last = encrypt_md5(password + salt)

            if last == merchant.password:
                return merchant.type
            else:
                return -1
    
    def verifyRedirectURL(self,redirect_uri):
        return True