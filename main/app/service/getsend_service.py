from app.models import db
from app.models.onlinetrades_dao import OnlinetradesDao,OnlinetradesExpansion
from app.models.merchant_dao import MerchantDao
from app.models.transaction_code_dao import Qrcode
import json,hashlib,requests,time
from app.models.notify_dao import NotifyDao
from flask_restful import abort
from sqlalchemy import and_
from flask import current_app
from app.common import keep_two_del

class GetsendService():
    def __init__(self,args):
        self.order_no = args['order_no']
        self.org_order_no = args['org_order_no']

    # 获取需要的数据
    def get_all_data(self):
        current_app.logger.info('补发通知开始获取数据')
        q = db.session.query(
            OnlinetradesDao.mer_code,
            OnlinetradesDao.order_no,
            OnlinetradesDao.org_order_no,
            OnlinetradesDao.audit_time,
            OnlinetradesDao.amount,
            OnlinetradesDao.bank_amount,
            OnlinetradesDao.pay_type,
            OnlinetradesDao.state,
            OnlinetradesExpansion.mer_notify_url,
            MerchantDao.secret_key,
        ).filter(and_(OnlinetradesDao.order_no == self.order_no,OnlinetradesDao.org_order_no == self.org_order_no,))
        q = q.outerjoin(OnlinetradesExpansion,and_(OnlinetradesExpansion.order_no == OnlinetradesDao.order_no,OnlinetradesExpansion.org_order_no == OnlinetradesDao.org_order_no))
        q = q.outerjoin(Qrcode, OnlinetradesDao.qr_code == Qrcode.code)
        q = q.outerjoin(MerchantDao,OnlinetradesDao.mer_code == MerchantDao.code)
        q = q.first()
        current_app.logger.info('补发通知查询数据集')
        if q is not None:
            if q.state==1 :
                return {
                    'success': False,
                    'errorCode': 410,
                    'errorMsg': '请先进行人工匹配在进行补发消息请求'
                }
            mer_code = q.mer_code
            if q.order_no is not None:
                order_no = q.order_no
            else:
                order_no = ''
            if q.audit_time:
                audit_time = q.audit_time
            else:
                audit_time = int(time.time())
            state = q.state
            payUrl = q.mer_notify_url
            org_order_no = q.org_order_no
            amount = keep_two_del(q.amount)
            real_amount = keep_two_del(q.bank_amount)
            pay_type = q.pay_type
            payUrl = q.mer_notify_url

            m_args = {}
            m_args['order_no'] = order_no
            m_args['mer_code'] = mer_code
            m_args['org_order_no'] = org_order_no
            m_args['amount'] = str(amount)
            m_args['real_amount'] = str(real_amount)
            m_args['pay_type'] = pay_type
            m_args['audit_time'] = audit_time
            m_args['state'] = state
            args = {}
            m_str = ''
            for k in sorted(m_args):
                args[k] = m_args[k]
                if m_args[k] is not None:
                    m_str += '%s=%s&' % (k,m_args[k])
            m_str = m_str[:-1]
            m_str +=  q.secret_key
            m_sign = self.get_sign(m_str)
            print('加密字符串:%s'%m_str)
            print('加密sign:%s'%m_sign)
            print('补发回调路由%s'%payUrl)
            current_app.logger.info('补发通知加密字符串%s' % m_str)
            current_app.logger.info('补发通知加密sign%s' % m_sign)
            m_args['sign'] = m_sign
            # 发送数据
            if payUrl is not None:
                url = payUrl + "?order_no=%s&org_order_no=%s&sign=%s&audit_time=%s&state=%s&amount=%s&real_amount=%s&pay_type=%s&mer_code=%s" % (order_no,org_order_no,m_sign, audit_time,state,amount,real_amount,pay_type,mer_code)
                print(url)
                headers = {'content-type': 'application/json'}
                response = requests.post(payUrl, data=json.dumps(m_args), headers=headers, timeout=30)
                print("返回")
                status_code = response.status_code
                m_res = response.text
                current_app.logger.info('获取回调信息%s' % m_res)
                if status_code < 400:
                    success = 1
                else:
                    success = 0
                return self.insert(args = args,status_code = status_code,m_res = m_res,order_no = order_no,success = success,mer_code = mer_code)
            else:
                return {
                    'success': False,
                    'errorCode': 404,
                    'errorMsg': '返回路径错误'
                }
        else:
            return {
                'success': False,
                'errorCode': 403,
                'errorMsg': '该订单不存在'
            }

    # 数据处理
    def get_sign(self,m_str):
        md = hashlib.md5()
        md.update((m_str).encode())
        m_sign = md.hexdigest()

        return m_sign


    def insert(self,args,status_code,m_res,order_no,mer_code,success=0):
        m_ar = {}
        m_ar['expansion_data'] = args
        m_ar['status_code'] = status_code
        m_ar['response'] = m_res
        m_ar['action_time'] = int(time.time())
        m_ar['order_no'] = order_no
        m_ar['success'] = success
        m_ar['mer_code'] = mer_code
        try:
            no = NotifyDao(**m_ar)
            db.session.add(no)
            db.session.commit()
            current_app.logger.info('同步notify')
        except Exception as e:
            db.session.rollback()
            db.session.remove()
            current_app.logger.exception(e)
            raise Exception(e)


