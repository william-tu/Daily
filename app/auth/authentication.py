# -*- coding: utf-8 -*-
from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth

from . import auth
from ..models import User
from ..responses import unauthorized

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email_or_token, password):
    if not email_or_token:
        return False
    if not password:
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.objects(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@basic_auth.error_handler
def auth_error():
    return unauthorized('unauthorized error')


@auth.route('/api/token',methods=['GET'])
@basic_auth.login_required
def token():
    if g.token_used:
        return unauthorized('invalid credentials')
    user = g.current_user
    print user.username
    return jsonify({'token': user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
