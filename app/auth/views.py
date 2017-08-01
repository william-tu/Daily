# -*- coding: utf-8 -*-
import random

from flask import session, request, g

from . import auth
from ..responses import bad_request, suc_response
from ..utils.mail import send_email
from ..models import User


@auth.route('/api/generate-code', methods=['POST'])
def generate_code():
    email = request.json.get('email')
    if not email:
        return bad_request('email is none')
    session['verify_code'] = random.randrange(1000, 10000)
    send_email(email, u'验证码', 'confirm/confirm', verify_code=session['verify_code'])
    return suc_response('send code successfully')


@auth.route('/api/register', methods=['POST'])
def register():
    info = request.json
    email = info.get('email')
    username = info.get('username')
    password = info.get('password')
    verify_code = info.get('verify_code')
    if not email or not username or not password or not verify_code:
        return bad_request('email or username or password or verify_code is empty')
    if verify_code != session.get('verify_code'):
        return bad_request('verify_code is wrong')
    if not session.get('useful_username') or not session.get('useful_username'):
        return bad_request('no verify')
    user = User(email=email, username=username)
    user.password = password
    user.save()
    return suc_response('register successfully')


@auth.route('/api/verify-username', methods=['POST'])
def username():
    username = request.json.get('username')
    user_by_name = User.objects(username=username).first()
    if user_by_name:
        session['useful_username'] = False
        return bad_request('username already has been exited')
    session['useful_username'] = True
    return suc_response('username is useful')


@auth.route('/api/verify-email', methods=['POST'])
def email():
    email = request.json.get('email')
    user_by_email = User.objects(email=email).first()
    if user_by_email:
        session['useful_email'] = False
        return bad_request('email already has been exited')
    session['useful_email'] = True
    return suc_response('email is useful')
