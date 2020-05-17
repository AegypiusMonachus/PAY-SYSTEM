from flask_restful import fields
from flask_sqlalchemy import Pagination


def make_fields(data_fields, **kwargs):
	result = {
		'success': fields.Boolean,
		'data': fields.List(fields.Nested(data_fields)),
		'page': fields.Integer,
		'pages': fields.Integer,
		'page_size': fields.Integer,
		'total': fields.Integer,
		'error_code': fields.Integer,
		'error_msg': fields.String,
	}
	for key in kwargs.keys():
		if key not in result:
			result[key] = kwargs[key]
	return result


def make_response(data=None, page=None, pages=None, total=None, error_code=None, error_message=None, **kwargs):
	result = {
		'success': data is not None,
		'data': data,
		'page': page,
		'pages': pages,
		'page_size': len(data) if data else None,
		'total': total,
		'error_code': error_code,
		'error_msg': error_message,
	}
	for key in kwargs.keys():
		if key not in result:
			result[key] = kwargs[key]
	return result


def make_response_from_pagination(pagination, **kwargs):
	if not isinstance(pagination, Pagination):
		raise TypeError
	return make_response(data=pagination.items, page=pagination.page, pages=pagination.pages, total=pagination.total, **kwargs)
