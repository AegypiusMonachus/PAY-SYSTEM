from . import db

class DfTradeAgentsDao(db.Model):
	__tablename__ = 'tb_df_trade_down'
	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	org_order_no = db.Column(db.String)
	account_name = db.Column(db.String)
	account_no = db.Column(db.String)
	bank_order_no = db.Column(db.String)
	mer_code = db.Column(db.String)
	amount = db.Column(db.Numeric, default=0)
	real_amount = db.Column(db.Numeric, default=0)
	action_time = db.Column(db.Integer)
	audit_time = db.Column(db.Integer)
	state = db.Column(db.Integer)
	free = db.Column(db.Numeric, default=0)
	sign = db.Column(db.String)
	state_code = db.Column(db.Integer)
	bankCd = db.Column(db.Integer)
	def get_data_by_order_no(self,order_no):
		return db.session.query(DfTradeAgentsDao).filter(DfTradeAgentsDao.order_no == order_no).first()


class DfTradeDao(db.Model):
	__tablename__ = 'tb_df_trade_up'

	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	org_order_no = db.Column(db.String)
	bank_order_no = db.Column(db.String)
	mer_code = db.Column(db.String)
	mer_username = db.Column(db.String)
	amount = db.Column(db.Numeric, default=0)
	real_amount = db.Column(db.Numeric, default=0)
	action_time = db.Column(db.Integer)
	audit_time = db.Column(db.Integer)
	sxf = db.Column(db.Numeric, default=0)
	state = db.Column(db.Integer)
	type = db.Column(db.Integer)
	bank_id = db.Column(db.Integer)
	account_name = db.Column(db.String)
	account_no = db.Column(db.String)
	real_sxf = db.Column(db.Numeric, default=0)
	sxf_detail = db.Column(db.JSON)
	
	def get_data_state1(self,mer_code,org_order_no):
		return db.session.query(DfTradeDao).filter(DfTradeDao.mer_code == mer_code,
				DfTradeDao.org_order_no == org_order_no).all()
				
	def get_data_state1_by_orderno(self,mer_code,order_no):
		return db.session.query(DfTradeDao).filter(DfTradeDao.mer_code == mer_code,
				DfTradeDao.order_no == order_no).all()


class DfTradeRechargeDao(db.Model):
	__tablename__ = 'tb_recharge_trade'

	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	bank_order_no = db.Column(db.String)
	amount = db.Column(db.Numeric, default=0)
	real_amount = db.Column(db.Numeric, default=0)
	action_time = db.Column(db.Integer)
	action_name = db.Column(db.String)
	audit_time = db.Column(db.Integer)
	audit_name = db.Column(db.String)
	df_bank_id = db.Column(db.Integer)
	df_bank_name = db.Column(db.String)
	account_name = db.Column(db.String)
	account_no = db.Column(db.String)
	state = db.Column(db.Integer)
	username = db.Column(db.String)
	mer_code = db.Column(db.String)
	remark = db.Column(db.String)


class DfTradeExpanDao(db.Model):
	__tablename__ = 'tb_df_trade_expansion'

	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	org_order_no = db.Column(db.String)
	expansion_data = db.Column(db.JSON)
	notify_url = db.Column(db.String)
	mer_code = db.Column(db.String)


	def get_data(self):
		res = db.session.query(
			DfTradeExpanDao.order_no,
			DfTradeExpanDao.org_order_no,
			DfTradeExpanDao.notify_url,
			DfTradeExpanDao.mer_code
		).all()
		result = []
		for i in res:
			result.append({
				'order_no':i.order_no,
				'org_order_no': i.org_order_no,
				'notify_url': i.notify_url,
				'mer_code': i.mer_code,
			})
		return	result

class DfQueryDetailDao(db.Model):
	__tablename__ = 'tb_df_query_details'
	id = db.Column(db.Integer, primary_key=True)
	mer_code = db.Column(db.String)
	mer_username = db.Column(db.String)
	order_no = db.Column(db.String)
	expansion_data = db.Column(db.JSON)
	action_time = db.Column(db.Integer)
	

class DfTradeSxfDao(db.Model):
	__tablename__ = 'tb_df_trade_sxf'

	id = db.Column(db.Integer, primary_key=True)
	mer_code = db.Column(db.String)
	agents_code = db.Column(db.String)
	mer_username = db.Column(db.String)
	agents_username = db.Column(db.String)
	sxf = db.Column(db.Numeric, default=0)
	order_no = db.Column(db.String)
	org_order_no = db.Column(db.String)
	action_time = db.Column(db.Integer)
	type = db.Column(db.Integer)



