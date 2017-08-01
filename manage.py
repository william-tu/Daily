# -*- coding: utf-8 -*-
from flask_script import Manager, Shell

from app import create_app, db
from app.models import Douban,User

app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db,Douban=Douban,User=User)

manager.add_command('shell',Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()