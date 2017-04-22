# -*- coding: utf-8 -*-
from flask import request,current_app,jsonify
from . import main
from ..models import Douban
from ..responses import forbbiden


@main.route('/api/article',methods=['POST'])
def hot():
    page = request.json.get('page',1)
    if  not isinstance(page,int):
        return forbbiden('type error')
    pagination = Douban.objects.paginate(page=page,per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource':[ i.to_json() for i in pagination.items],
        'next': pagination.has_next,
        'pages':pagination.pages
    })