from app.api_0_1.parsers.refulation_parser import refulationParsers
from flask_restful import Resource, marshal_with, fields
from app.service.regulation_service import getdate,insert,update
from app.api_0_1.common import make_fields, make_response

class refulationApi(Resource):
    def get(self):
        res = getdate()
        result = []
        result.append({
            "id": res.id if res else None,
            "stop_service": res.stop_service if res else None,
            "exempt": res.exempt if res else None,
            "notify_times": res.notify_times if res else None,
            "pay_times": res.pay_times if res else None,
            "pay_url_times": res.pay_url_times if res else None,
            "perday_income": res.perday_income if res else None,
            "repetition_time": res.repetition_time if res else None,
            "large_limit_lower": res.large_limit_lower if res else None,
            "large_limit_upper": res.large_limit_upper if res else None,
            "small_limit_lower": res.small_limit_lower if res else None,
            "small_limit_upper": res.small_limit_upper if res else None
        })
        return make_response(result)
    def put(self):
        m_args = refulationParsers.parse_args(strict=True)
        res = getdate()
        if res is None:
            res = insert()
        id = res.id
        m_args['id'] = id
        up = update(m_args)
        res = getdate()
        result = []
        result.append({
            "id": res.id if res else None,
            "stop_service": res.stop_service if res else None,
            "exempt": res.exempt if res else None,
            "notify_times": res.notify_times if res else None,
            "pay_times": res.pay_times if res else None,
            "pay_url_times": res.pay_url_times if res else None,
            "perday_income": res.perday_income if res else None,
            "repetition_time": res.repetition_time if res else None,
            "large_limit_lower": res.large_limit_lower if res else None,
            "large_limit_upper": res.large_limit_upper if res else None,
            "small_limit_lower": res.small_limit_lower if res else None,
            "small_limit_upper": res.small_limit_upper if res else None
        })
        return make_response(result)



