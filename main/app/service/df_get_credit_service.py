from app.models import db
from app.models.df_trade_dao import DfTradeRechargeDao


class DfGetCreditSer():

	def get_data(self, critern, page=None,per_page=None):
		q = db.session.query(
			DfTradeRechargeDao.id,
			DfTradeRechargeDao.order_no,
			DfTradeRechargeDao.username,
			DfTradeRechargeDao.amount,
			DfTradeRechargeDao.state,
			DfTradeRechargeDao.action_time,
			DfTradeRechargeDao.audit_time,
			DfTradeRechargeDao.remark,
			DfTradeRechargeDao.audit_name
		).filter(*critern).order_by(DfTradeRechargeDao.action_time.desc())
		q = q.paginate(page, per_page, error_out=False)
		return q