from flask_restful import Resource
from app.service.resports_service import GetResports
from ..common import make_response
from app.common import keep_two_del

class Resports(Resource):
    def get(self):
        resports = GetResports()
        res_args = resports.get_resports_info()
        result = []
        for res in res_args:
            if res.cost_agent_day is not None:
                cost_agent_day = float('%.2f' % keep_two_del(res.cost_agent_day))
            else:
                cost_agent_day = 0

            if res.cost_agent_service_day is not None:
                cost_agent_service_day = float('%.2f' % keep_two_del(res.cost_agent_service_day))
            else:
                cost_agent_service_day = 0

            if res.withdraw_agent_amount_day is not None:
                withdraw_agent_amount_day = float('%.2f' % keep_two_del(res.withdraw_agent_amount_day))
            else:
                withdraw_agent_amount_day = 0

            if res.cost_agent_yes is not None:
                cost_agent_yes = float('%.2f' % keep_two_del(res.cost_agent_yes))
            else:
                cost_agent_yes = 0

            if res.cost_agent_service_yes is not None:
                cost_agent_service_yes = float('%.2f' % keep_two_del(res.cost_agent_service_yes))
            else:
                cost_agent_service_yes = 0

            if res.withdraw_agent_amount_yes is not None:
                withdraw_agent_amount_yes = float('%.2f' % keep_two_del(res.withdraw_agent_amount_yes))
            else:
                withdraw_agent_amount_yes = 0

            if res.cost_agent_thisweek is not None:
                cost_agent_thisweek = float('%.2f' % keep_two_del(res.cost_agent_thisweek))
            else:
                cost_agent_thisweek = 0

            if res.cost_agent_service_thisweek is not None:
                cost_agent_service_thisweek = float('%.2f' % keep_two_del(res.cost_agent_service_thisweek))
            else:
                cost_agent_service_thisweek = 0

            if res.withdraw_agent_amount_thisweek is not None:
                withdraw_agent_amount_thisweek = float('%.2f' % keep_two_del(res.withdraw_agent_amount_thisweek))
            else:
                withdraw_agent_amount_thisweek = 0

            if res.cost_agent_thismonth is not None:
                cost_agent_thismonth = float('%.2f' % keep_two_del(res.cost_agent_thismonth))
            else:
                cost_agent_thismonth = 0

            if res.cost_agent_service_thismonth is not None:
                cost_agent_service_thismonth = float('%.2f' % keep_two_del(res.cost_agent_service_thismonth))
            else:
                cost_agent_service_thismonth = 0

            if res.withdraw_agent_amount_thismonth is not None:
                withdraw_agent_amount_thismonth = float('%.2f' % keep_two_del(res.withdraw_agent_amount_thismonth))
            else:
                withdraw_agent_amount_thismonth = 0

            if res.bank_amount_day_member is not None:
                bank_amount_day_member = float('%.2f' % keep_two_del(res.bank_amount_day_member))
            else:
                bank_amount_day_member = 0

            if res.withdraw_amount_day_member is not None:
                withdraw_amount_day_member = float('%.2f' % keep_two_del(res.withdraw_amount_day_member))
            else:
                withdraw_amount_day_member = 0

            if res.bank_amount_yes_member is not None:
                bank_amount_yes_member = float('%.2f' % keep_two_del(res.bank_amount_yes_member))
            else:
                bank_amount_yes_member = 0

            if res.withdraw_amount_yes_member is not None:
                withdraw_amount_yes_member = float('%.2f' % keep_two_del(res.withdraw_amount_yes_member))
            else:
                withdraw_amount_yes_member = 0

            if res.bank_amount_thisweek_member is not None:
                bank_amount_thisweek_member = float('%.2f' % keep_two_del(res.bank_amount_thisweek_member))
            else:
                bank_amount_thisweek_member = 0

            if res.withdraw_amount_thisweek_member is not None:
                withdraw_amount_thisweek_member = float('%.2f' % keep_two_del(res.withdraw_amount_thisweek_member))
            else:
                withdraw_amount_thisweek_member = 0

            if res.bank_amount_thismonth_member is not None:
                bank_amount_thismonth_member = float('%.2f' % keep_two_del(res.bank_amount_thismonth_member))
            else:
                bank_amount_thismonth_member = 0

            if res.withdraw_amount_thismonth_member is not None:
                withdraw_amount_thismonth_member = float('%.2f' % keep_two_del(res.withdraw_amount_thismonth_member))
            else:
                withdraw_amount_thismonth_member = 0

            # -----------------------------------------------------------------------------------------
            if res.pt_day is not None:
                pt_day = float('%.2f' % keep_two_del(res.pt_day))
            else:
                pt_day = 0

            if res.pt_yes is not None:
                pt_yes = float('%.2f' % keep_two_del(res.pt_yes))
            else:
                pt_yes = 0

            if res.pt_thisweek is not None:
                pt_thisweek = float('%.2f' % keep_two_del(res.pt_thisweek))
            else:
                pt_thisweek = 0

            if res.pt_thismonth is not None:
                pt_thismonth = float('%.2f' % keep_two_del(res.pt_thismonth))
            else:
                pt_thismonth = 0

            result.append({
                'cost_agent_day':cost_agent_day,
                'cost_agent_service_day': cost_agent_service_day,
                'withdraw_agent_amount_day': withdraw_agent_amount_day,
                'cost_agent_yes': cost_agent_yes,
                'cost_agent_service_yes': cost_agent_service_yes,
                'withdraw_agent_amount_yes': withdraw_agent_amount_yes,
                'cost_agent_thisweek': cost_agent_thisweek,
                'cost_agent_service_thisweek': cost_agent_service_thisweek,
                'withdraw_agent_amount_thisweek': withdraw_agent_amount_thisweek,
                'cost_agent_thismonth': cost_agent_thismonth,
                'cost_agent_service_thismonth': cost_agent_service_thismonth,
                'withdraw_agent_amount_thismonth': withdraw_agent_amount_thismonth,
                'bank_amount_day_member': bank_amount_day_member,
                'withdraw_amount_day_member': withdraw_amount_day_member,
                'bank_amount_yes_member': bank_amount_yes_member,
                'withdraw_amount_yes_member': withdraw_amount_yes_member,
                'bank_amount_thisweek_member': bank_amount_thisweek_member,
                'withdraw_amount_thisweek_member': withdraw_amount_thisweek_member,
                'bank_amount_thismonth_member': bank_amount_thismonth_member,
                'withdraw_amount_thismonth_member': withdraw_amount_thismonth_member,

                'pt_day': pt_day,
                'pt_yes': pt_yes,
                'pt_thisweek': pt_thisweek,
                'pt_thismonth': pt_thismonth,

            })

        return make_response(result)