# -*- coding: utf-8 -*-
from . import main
from ..responses import not_found, forbbiden, bad_request, method_not_allowed, internal_server_error


@main.errorhandler(404)
def page_not_found(e):
    return not_found('not found')


@main.errorhandler(403)
def forbbiden(e):
    return forbbiden('forbbiden')


@main.errorhandler(405)
def method_not_allowed(e):
    return method_not_allowed('method not allowed')


@main.errorhandler(400)
def bad_request(e):
    return bad_request('bad request')


@main.app_errorhandler(500)
def internal_server_error(e):
    return internal_server_error('internal server error')
