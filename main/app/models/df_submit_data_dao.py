from . import db


class DfSubData(db.Model):
    __tablename__ = 'tb_df_submit_data'

    id = db.Column(db.Integer, primary_key=True)
    df_url = db.Column(db.String)
    select_key = db.Column(db.String)
    code = db.Column(db.String)
    query_url = db.Column(db.String)


    def get_data(self):
        res = db.session.query(DfSubData).first()
        return res