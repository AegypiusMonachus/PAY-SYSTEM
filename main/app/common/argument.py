from flask_restful import reqparse


class Argument(reqparse.Argument):
    """
    继承自 reqparse.Argument, 增加 nullable 关键字参数，
    对于值为 None 并且 nullable=False 的字段 raise TypeError
    """
    def __init__(self, name, default=None, dest=None, required=False,
                 ignore=False, type=reqparse.text_type,
                 location=('json', 'values',), choices=(),
                 action='store', help=None, operators=('=',),
                 case_sensitive=True, nullable=False):
        self.nullable = nullable
        super(Argument, self).__init__(name, default=default, dest=dest,
                                       required=required, ignore=ignore,
                                       type=type, location=location,
                                       choices=choices, action=action,
                                       help=help, operators=operators,
                                       case_sensitive=case_sensitive)

    def convert(self, value, op):
        if value is None and not self.nullable:
            raise TypeError("%s can't be null" % self.name)
        return super(Argument, self).convert(value, op)