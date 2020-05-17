from flask_restful import Resource
from app.models import db
from app.models.df_agent_rate_dao import DfAgentRate
from flask_restful.reqparse import RequestParser
from app.models.df_trade_dao import DfTradeDao
from sqlalchemy import func,and_
import decimal
from app.common import keep_two_del

class TestAmount(Resource):


    def get(self):
        mer_code = '155fe8ce7e4e42efa72d2e2b45809194'
        result = self.calculation_amount(mer_code)
        sxf = 0
        for res in result:
            sxf_g = decimal.Decimal(str(res['sxf_g']))
            sxf_q = decimal.Decimal(str(res['sxf']))
            am = sxf_g + sxf_q
            sxf += am
        sxf = float('%.2f' % keep_two_del(sxf))
        return sxf

    def calculation_amount(self,mer_code):
        amount = 500
        res = db.session.query(DfAgentRate).filter(DfAgentRate.mer_code == mer_code).all()
        asm = db.session.query(func.sum(DfTradeDao.amount)).filter(and_(DfTradeDao.mer_code == mer_code, DfTradeDao.state == 2)).first()
        if asm is None:
            asm = 0
        rs = {}
        rs_g = {}
        rs_name = {}
        res_r = []
        for i in res:
            yhjeDict = {}
            yhLists = []
            # 根据存款金额进行排序
            for args in i.rate_amount:
                yhLists.append(args)
            yhLists.sort(key=lambda x: float(x["amount"]))
            yhLists.reverse()
            rs['%s' % i.agent_code] = yhLists
            rs_g['%s' % i.agent_code] = i.rate_prop
            rs_name['%s' % i.agent_code] = i.agent_name
            res_r.append(i.agent_code)
        print('***********************************************************')
        print(rs)
        print('***********************************************************')
        sxf_sum = 0
        result = []
        for i in res_r:
            res_di = {}
            print('该商户的总成交的订单金额%s' % asm)
            if asm is not None:
                asm = float('%.3f' % asm)
            rate = rs[i]
            agent_name = rs_name[i]
            # rate_g = float('%.3f' % rs_g[i])
            rate_g = rs_g[i]
            sxf_on = 0
            print(amount, type(amount))
            print(rate_g, type(rate_g))
            # sxf_g = decimal.Decimal(str(res['rate_g']))
            sxf_g = amount * rate_g
            print('代理%s的固定手续费%s' % (i, sxf_g))
            res_di['agents_code'] = i
            res_di['agents_name'] = agent_name
            res_di['sxf_g'] = sxf_g
            for j in rate:
                sxf = 0
                sxf += j['amount']
                res_di['sxf'] = sxf
                break
            result.append(res_di)
            print('返回字段%s' % result)
            sxf = decimal.Decimal(str(sxf))
            sxf_sum += sxf + sxf_g
        print('代付总手续飞%s' % sxf_sum)
        return result