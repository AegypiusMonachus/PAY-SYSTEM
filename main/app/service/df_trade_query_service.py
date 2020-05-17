from app.service.w_onlinetride_service import WOlinetrideService
import json, hashlib, requests, time
from app.models import db
from app.models.df_trade_dao import DfTradeAgentsDao, DfTradeDao, DfQueryDetailDao,DfTradeExpanDao,DfTradeSxfDao
from app.models.merchant_dao import MerchantDao
from app.models.df_submit_data_dao import DfSubData
from app.log import agentpayQuerylogger
# from Crypto.SelfTest.Signature.test_dss import res
from app.common import formatDecimal,date_to_int,keep_two_del
from app.models.notify_dao import DfNotifyDao
from .merchant_service import getDataByCode
from app.common import formatDecimal
from decimal import Decimal
import decimal
class DFQueryDetailService():
    def __init__(self, args):
        #上游参数
        self.__args_up = args
        self.success = True
        self.error_code = None
        self.error_msg = None
        self.__subdataDao = None
        self.__tradedataDao = None
        self.__merchantDao = None
        self.sign = None
    
    def queryDetail(self):
        try:
            self.__merchantDao = getDataByCode(self.__args_up['mer_code'])
            if not self.__merchantDao:
                self.success = False
                self.error_msg = '账户号错误'
                self.error_code = 8101
                return 
            self.__tradedataDao = DfTradeDao().get_data_state1(self.__merchantDao.code,self.__args_up['org_order_no'])
            m_size = len(self.__tradedataDao)
            if m_size != 1:
                self.success = False
                self.error_msg = '订单号错误'
                self.error_code = 8102
                agentpayQuerylogger.info("订单号错误 : %s"%(self.__args_up['org_order_no']))
                return 
            sign = self.__args_up.pop('sign')
            m_sign = self.credit_sign(self.__args_up, self.__merchantDao.secret_key)
            m_sign = self.get_sign(m_sign)
            if m_sign != sign:
                self.success = False
                self.error_msg = '签名不正确'
                self.error_code = 8103
                agentpayQuerylogger.info("签名不正确 .%s,%s"%(sign,m_sign))
                return 
            audit_time = int(time.time())
            trade = self.__tradedataDao[0]
            m_result = {}
            m_result['mer_code'] = self.__args_up['mer_code']
            m_result['order_no'] = trade.order_no
            m_result['org_order_no'] = trade.org_order_no
            m_result['state'] = trade.state
            m_result['audit_time'] = trade.audit_time
            m_result['amount'] = str(keep_two_del(trade.amount))
            m_result['sxf'] = str(keep_two_del(trade.real_sxf))
            m_sign = self.credit_sign(m_result, self.__merchantDao.secret_key)
            m_sign = self.get_sign(m_sign)
            m_result['sign'] = m_sign
            return m_result
#             if trade.state == 1:
#                 self.____subdataDao = DfSubData().get_data()
#                 df_query_url =  self.____subdataDao.query_url
#                 df_query_skey =  self.____subdataDao.select_key
#                 df_quer_mcode =  self.____subdataDao.code
#                 agentpayQuerylogger.info("%s 订单号查询"%(trade.order_no))
#                 mdata = {}
#                 mdata['mchntCd'] = df_quer_mcode
#                 mdata['mchntPayforSsn'] = trade.order_no
#                 mstr = "mchntCd=%s&mchntPayforSsn=%s%s"%(df_quer_mcode,trade.order_no,df_query_skey)
#                 mdata['sign'] = self.get_sign(mstr)
#                 #代付交易查询
#                 agentpayQuerylogger.info("向下游发送查询请求")
#                 res_json = self.cash_post(mdata, df_query_url)
#                 res_sign = res_json.pop('sign')
#                 m_sign = self.credit_sign(res_json, df_query_skey)
#                 m_sign = self.get_sign(m_sign)
#                 if res_sign != m_sign:
#                     raise Exception('下游接口验签失败  :  res_sign = %s , m_sign = %s'%(res_sign,m_sign))
#                 #判断交易状态是否更新
#                 if int(res_json['paySt']) == trade.state or int(res_json['paySt'] == 0) :
#                     agentpayQuerylogger.error("%s订单状态没有改变，不需要更新"%(trade.order_no))
#                 else:
#                     agentpayQuerylogger.error("%s订单状态改变，进行更新"%(trade.order_no))
#                     self.insert_query_detail(res_json, trade, audit_time)
#                     self.update(res_json, trade, audit_time)
#             m_result = {}
#             m_result['mer_code'] = self.__args_up['mer_code']
#             m_result['order_no'] = trade.order_no
#             m_result['org_order_no'] = trade.org_order_no
#             m_result['state'] = trade.state
#             m_result['audit_time'] = trade.audit_time
#             m_result['amount'] = str(keep_two_del(trade.amount))
#             m_result['sxf'] = str(keep_two_del(trade.real_sxf))
#             m_sign = self.credit_sign(m_result, self.__merchantDao.secret_key)
#             m_sign = self.get_sign(m_sign)
#             m_result['sign'] = m_sign
#             return m_result
        except Exception as e:
            agentpayQuerylogger.exception(e)
            agentpayQuerylogger.error(format(e))
            self.success = False
            self.error_msg = '代付通道维护'
            self.error_code = 8199
            return
    
    def insert_query_detail(self,mdata, tradedata,audit_time):
        try:
            querydata = DfQueryDetailDao()
            querydata.mer_code = tradedata.mer_code
            querydata.mer_username = tradedata.mer_username
            querydata.order_no = tradedata.order_no
            querydata.expansion_data = mdata
            querydata.action_time = audit_time
            db.session.add(querydata)
            db.session.commit()
        except Exception as e:        
            agentpayQuerylogger.exception(e)
            agentpayQuerylogger.error("QueryDetail保存失败:%s"%(mdata))
            
    def insert_sxf_detail(self,sxf,type,trade,audit_time):
        sxf_dao = DfTradeSxfDao()
        sxf_dao.mer_code = trade.mer_code
        sxf_dao.mer_username = trade.mer_username
        sxf_dao.agents_code = sxf['agents_code']
        sxf_dao.agents_username = sxf['agents_name']
        sxf_dao.order_no = trade.order_no
        sxf_dao.org_order_no = trade.org_order_no
        sxf_dao.action_time = audit_time
        if type == 1:
            sxf_dao.type = 1
            sxf_dao.sxf = decimal.Decimal(sxf['sxf_g'])
        elif type == 2:
            sxf_dao.type = 2
            sxf_dao.sxf = decimal.Decimal(sxf['sxf'])
        db.session.add(sxf_dao)
            
     
    def get_sign(self,m_str):
        try:
            agentpayQuerylogger.info("加密前 : %s"%(m_str))
            md = hashlib.md5()
            md.update((m_str).encode())
            m_sign = md.hexdigest()
            agentpayQuerylogger.info("加密后 : %s"%(m_sign))
            return m_sign
        except Exception as e:
            agentpayQuerylogger.exception(e)
            agentpayQuerylogger.error("签名错误:%s"%(format(e)))
            return None
     
    def cash_post(self,data_args, pay_url):
        try:
            res_json = None
            agentpayQuerylogger.info("下游请求地址 %s,请求参数 %s"%(pay_url,data_args))
            headers = {'content-type': 'application/json'}
            r = requests.post(pay_url, data=json.dumps(data_args), headers=headers)
            status_code = r.status_code
            res = r.text
            if(status_code >= 400):
                agentpayQuerylogger.error("接口返回错误 : %s"%(res))
                raise Exception('下游接口返回错误 : %s'%(res_json))
            agentpayQuerylogger.info("接口返回正确 : %s"%(res))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            agentpayQuerylogger.exception(e)
            agentpayQuerylogger.error("下游查询订单错误 : %s"%(format(e)))
            raise Exception('下游接口返回错误 : %s'%(res_json))
     
    def update(self,res_json,trade,audit_time):
        agentpayQuerylogger.info("%s订单更新"%(trade.order_no))
        self.__merchantDao.dongjie_amount = self.__merchantDao.dongjie_amount - trade.amount - trade.sxf
        try:
            res_state = int(res_json['paySt'])
            trade_down = DfTradeAgentsDao().get_data_by_order_no(trade.order_no)
            trade.state = res_state
            trade_down.state = res_state
            if res_json['fee']:
                trade.free = formatDecimal(res_json['fee'])
                trade_down.free = formatDecimal(res_json['fee'])
            if res_json['txnDt']:
                timesp = date_to_int(res_json['txnDt'])
                trade.audit_time = timesp
                trade_down.audit_time = timesp
            if res_json['txnId']:
                trade.bank_order_no = res_json['txnId']
                trade_down.bank_order_no = res_json['txnId']
            if res_json['destAmount']:
                trade.real_amount = formatDecimal(res_json['destAmount'])/100
                trade_down.real_amount = formatDecimal(res_json['destAmount'])/100
            if trade.state == 3:
                self.__merchantDao.amount = self.__merchantDao.amount + trade.amount + trade.sxf
            if trade.state == 2:
                agentpayQuerylogger.info("重新计算手续费")
                sxf_list = WOlinetrideService.calculation_amount(trade.mer_code,trade.amount)
                real_sxf = 0
                if len(sxf_list) > 0:
                    for sxf in sxf_list:
                        agent_sxf = 0
                        if 'sxf_g' in sxf:
                            real_sxf += decimal.Decimal(sxf['sxf_g'])
                            agent_sxf += decimal.Decimal(sxf['sxf_g'])
                            self.insert_sxf_detail(sxf, 1,trade, audit_time)
                        if 'sxf' in sxf:
                            real_sxf += decimal.Decimal(sxf['sxf'])
                            agent_sxf += decimal.Decimal(sxf['sxf'])
                            self.insert_sxf_detail(sxf, 2,trade, audit_time)
                        if agent_sxf > 0:
                            agent_dao = getDataByCode(sxf['agents_code'])
                            agent_dao.amount += agent_sxf
                            db.session.add(agent_dao)
                    trade.sxf_detail = sxf_list
                trade.real_sxf = real_sxf
                if trade.sxf != trade.real_sxf:
                    m_limit = trade.sxf - trade.real_sxf
                    agentpayQuerylogger.info("手续费差值 : %s"%(m_limit))
                    self.__merchantDao.amount += m_limit
                db.session.add(trade)
            db.session.add(trade)
            db.session.add(trade_down)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.remove()
            agentpayQuerylogger.exception(e)
            agentpayQuerylogger.error("%s订单更新失败"%(trade.order_no))
        
        
    # 回调上游的函数
#     def send_notify(self,trade,audit_time):
#         agentpayQuerylogger.info("%s消息通知"%(trade.order_no))
#         try:
#             trade_expansion_dao = db.session.query(DfTradeExpanDao,MerchantDao.secret_key).filter(
#                                     trade.order_no == DfTradeExpanDao.order_no,
#                                     trade.mer_code == DfTradeExpanDao.mer_code,
#                                     MerchantDao.code == DfTradeExpanDao.mer_code).first()
#             m_data = {}
#             success = 1
#             m_url = trade_expansion_dao.notify_url
#             m_data['mer_code'] = trade.mer_code
#             m_data['order_no'] = trade.order_no
#             m_data['org_order_no'] = trade.org_order_no
#             m_data['audit_time'] = audit_time
#             m_data['amount'] = trade.amount
#             m_data['sxf'] = trade.sxf
#             m_data['state'] = trade.state
#             m_sign = credit_sign(m_data,trade_expansion_dao.secret_key)
#             m_data['sign'] = m_sign
#             agentpayQuerylogger.info("URL:%s"%(m_url))
#             agentpayQuerylogger.info("参数:%s"%(m_data))
#             headers = {'content-type': 'application/json'}
#             response = requests.post(m_url, data=json.dumps(m_data), headers=headers)
#             status_code = response.status_code
#             m_res = response.text
#             if status_code >= 400:
#                 status_code = 0
#             agentpayQuerylogger.info('接口返回 : %s' % m_res)
#             insert_dfNotify_notice(m_data,success,status_code,m_res)
#             return True
#         except Exception as e:
#             agentpayQuerylogger.exception(e)
#             agentpayQuerylogger.error("消息通知失败 : %s"%(format(e)))
#             return False
        
        
    # 生成加密字符串
    def credit_sign(self,m_args,select_key):
        m_str = ''
        for k in sorted(m_args):
            if m_args[k] is not None:
                m_str += '%s=%s&' % (k, m_args[k])
        m_str = m_str[:-1]
        m_str = m_str + select_key
        return m_str
    
    
    def insert_dfNotify_notice(self,m_data,success,status_code,m_res):
        m_ar = {}
        m_ar['expansion_data'] = m_data
        m_ar['status_code'] = status_code
        m_ar['response'] = m_res
        m_ar['action_time'] = int(time.time())
        m_ar['order_no'] = m_data['order_no']
        m_ar['success'] = success
        m_ar['mer_code'] = m_data['mer_code']
        try:
            no = DfNotifyDao(**m_ar)
            db.session.add(no)
            db.session.commit()
            agentpayQuerylogger.info('同步df_notify')
        except Exception as e:
            db.session.rollback()
            db.session.remove()
            agentpayQuerylogger.exception(e)

    
    def updateDetailByAdmin(self):
        audit_time = int(time.time())
        self.__merchantDao = getDataByCode(self.__args_up['mer_code'])
        if not self.__merchantDao:
            self.success = False
            self.error_msg = '账户号错误'
            self.error_code = 8101
            return 
        self.__tradedataDao = DfTradeDao().get_data_state1_by_orderno(self.__merchantDao.code,self.__args_up['order_no'])
        m_size = len(self.__tradedataDao)
        if m_size != 1:
            self.success = False
            self.error_msg = '订单号错误'
            self.error_code = 8102
            agentpayQuerylogger.info("订单号错误 : %s"%(self.__args_up['order_no']))
            return 
        trade = self.__tradedataDao[0]
        self.__merchantDao.dongjie_amount = self.__merchantDao.dongjie_amount - trade.amount - trade.sxf
        if self.__args_up['state'] == 3 and trade.state != 3:
            self.__merchantDao.amount = self.__merchantDao.amount + trade.amount + trade.sxf
        elif self.__args_up['state'] == 2 and trade.state == 1:
            agentpayQuerylogger.info("重新计算手续费")
            sxf_list = WOlinetrideService.calculation_amount(trade.mer_code,trade.amount)
            real_sxf = 0
            if len(sxf_list) > 0:
                for sxf in sxf_list:
                    agent_sxf = 0
                    if 'sxf_g' in sxf:
                        real_sxf += decimal.Decimal(sxf['sxf_g'])
                        agent_sxf += decimal.Decimal(sxf['sxf_g'])
                        self.insert_sxf_detail(sxf, 1,trade, audit_time)
                    if 'sxf' in sxf:
                        real_sxf += decimal.Decimal(sxf['sxf'])
                        agent_sxf += decimal.Decimal(sxf['sxf'])
                        self.insert_sxf_detail(sxf, 2,trade, audit_time)
                    if agent_sxf > 0:
                        agent_dao = getDataByCode(sxf['agents_code'])
                        agent_dao.amount += agent_sxf
                        db.session.add(agent_dao)
                trade.sxf_detail = sxf_list
            trade.real_sxf = real_sxf
            if trade.sxf != trade.real_sxf:
                m_limit = trade.sxf - trade.real_sxf
                agentpayQuerylogger.info("手续费差值 : %s"%(m_limit))
                self.__merchantDao.amount += m_limit
        else :
            self.success = False
            self.error_msg = '更新失败'
            self.error_code = 8199
            agentpayQuerylogger.error("%s订单更新失败 , 从state %s 更新到 %s"%(trade.order_no,trade.state,self.__args_up['state']))
        trade.state = self.__args_up['state']
        trade.audit_time = audit_time
        db.session.add(trade)
        db.session.add(self.__merchantDao)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.remove()
            agentpayQuerylogger.exception(e)
            agentpayQuerylogger.error("%s订单更新失败"%(trade.order_no))
            self.success = False
            self.error_msg = '更新失败'
            self.error_code = 8199