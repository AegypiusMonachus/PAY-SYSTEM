import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import time


formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s | %(module)s | %(lineno)d | %(funcName)s | %(message)s')

paylogger = logging.getLogger("paylog")
payhandler = TimedRotatingFileHandler(filename='logs/paylog.log', when='MIDNIGHT', backupCount=7, atTime=time(0, 0, 0, 0))
payhandler.setFormatter(formatter)
paylogger.addHandler(payhandler)
paylogger.setLevel('INFO')

banklogger = logging.getLogger("banklog")
bankhandler = TimedRotatingFileHandler(filename='logs/banklog.log', when='MIDNIGHT', backupCount=7, atTime=time(0, 0, 0, 0))
bankhandler.setFormatter(formatter)
banklogger.addHandler(bankhandler)
banklogger.setLevel('INFO')

agentpaylogger = logging.getLogger("agentpaylog")
agentpayhandler = TimedRotatingFileHandler(filename='logs/agentpaylog.log', when='MIDNIGHT', backupCount=7, atTime=time(0, 0, 0, 0))
agentpayhandler.setFormatter(formatter)
agentpaylogger.addHandler(agentpayhandler)
agentpaylogger.setLevel('INFO')

agentpayQuerylogger = logging.getLogger("agentpayQuerylog")
agentpayQueryhandler = TimedRotatingFileHandler(filename='logs/agentpayQuerylog.log', when='MIDNIGHT', backupCount=7, atTime=time(0, 0, 0, 0))
agentpayQueryhandler.setFormatter(formatter)
agentpayQuerylogger.addHandler(agentpayQueryhandler)
agentpayQuerylogger.setLevel('INFO')
