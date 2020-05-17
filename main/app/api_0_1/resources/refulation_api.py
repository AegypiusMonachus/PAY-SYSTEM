from ..parsers.refulation_parser import refulationParsers
from flask_restful import Resource, marshal_with, fields
from app.service.regulation_service import getdate,insert,update,get_default_agent
from ..common import make_fields, make_response
from app.common import keep_two_del

class refulationApi(Resource):
    def get(self):
        res = getdate()
        result = []
        if res.large_limit_lower is not None:
            large_limit_lower = float('%.2f' % keep_two_del(res.large_limit_lower))
        else:
            large_limit_lower = 0

        if res.large_limit_upper is not None:
            large_limit_upper = float('%.2f' % keep_two_del(res.large_limit_upper))
        else:
            large_limit_upper = 0

        if res.small_limit_lower is not None:
            small_limit_lower = float('%.2f' % keep_two_del(res.small_limit_lower))
        else:
            small_limit_lower = 0

        if res.small_limit_upper is not None:
            small_limit_upper = float('%.2f' % keep_two_del(res.small_limit_upper))
        else:
            small_limit_upper = 0

        if res.perday_income is not None:
            perday_income = float('%.2f' % keep_two_del(res.perday_income))
        else:
            perday_income = 0
        result.append({
            "id": res.id if res else None,
            "agents": res.agents if res else None,
            "stop_service": res.stop_service if res else None,
            "exempt": res.exempt if res else None,
            "notify_times": res.notify_times if res else None,
            "pay_times": res.pay_times if res else None,
            "pay_url_times": res.pay_url_times if res else None,
            "perday_income":perday_income,
            "repetition_time": res.repetition_time if res else None,
            "large_limit_lower": large_limit_lower,
            "large_limit_upper": large_limit_upper,
            "small_limit_lower": small_limit_lower,
            "small_limit_upper": small_limit_upper
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
        if res.large_limit_lower is not None:
            large_limit_lower = float('%.2f' % keep_two_del(res.large_limit_lower))
        else:
            large_limit_lower = 0

        if res.large_limit_upper is not None:
            large_limit_upper = float('%.2f' % keep_two_del(res.large_limit_upper))
        else:
            large_limit_upper = 0

        if res.small_limit_lower is not None:
            small_limit_lower = float('%.2f' % keep_two_del(res.small_limit_lower))
        else:
            small_limit_lower = 0

        if res.small_limit_upper is not None:
            small_limit_upper = float('%.2f' % keep_two_del(res.small_limit_upper))
        else:
            small_limit_upper = 0

        if res.perday_income is not None:
            perday_income = float('%.2f' % keep_two_del(res.perday_income))
        else:
            perday_income = 0
        result.append({
            "id": res.id if res else None,
            "agents": res.agents if res else None,
            "stop_service": res.stop_service if res else None,
            "exempt": res.exempt if res else None,
            "notify_times": res.notify_times if res else None,
            "pay_times": res.pay_times if res else None,
            "pay_url_times": res.pay_url_times if res else None,
            "perday_income": perday_income,
            "repetition_time": res.repetition_time if res else None,
            "large_limit_lower": large_limit_lower,
            "large_limit_upper": large_limit_upper,
            "small_limit_lower": small_limit_lower,
            "small_limit_upper": small_limit_upper
        })
        return make_response(result)




class GetDefaultAgents(Resource):
    def get(self):
        res = get_default_agent()
        result = []
        for i in res:
            result.append({
                'name':i.username
            })
        return make_response(result)

