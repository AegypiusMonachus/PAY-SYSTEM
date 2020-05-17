from flask_restful.reqparse import RequestParser
from ..utils import *



dfagentskkparser = RequestParser(trim=True)
dfagentskkparser.add_argument('page', type=int)
dfagentskkparser.add_argument('page_size', type=int)

dfagentskkparser.add_argument('mer_code', type=str)
dfagentskkparser.add_argument('username', type=str)
dfagentskkparser.add_argument('begin_time', type=int)
dfagentskkparser.add_argument('end_time', type=int)
dfagentskkparser.add_argument('state', type=int)