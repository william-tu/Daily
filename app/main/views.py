# -*- coding: utf-8 -*-
from math import ceil

from flask import request, current_app, jsonify, render_template, g

from . import main
from .. import client
from ..models import Douban, Guoke, Zhihu
from ..auth.authentication import basic_auth
from ..responses import suc_response

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@main.route('/query', methods=['GET', 'POST'])
def query():
    keywords = request.args.get('keywords')
    return render_template('search.html', keywords=keywords)


@main.route('/api/douban/article', methods=['GET'])
def douban():
    page = request.args.get('page', 1, type=int)
    pagination = Douban.objects.paginate(page=page, per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource': [i.to_json() for i in pagination.items],
        'has_next': pagination.has_next,
        'pages': pagination.pages
    })


@main.route('/api/guoke/article', methods=['GET'])
def guoke():
    page = request.args.get('page', 1, type=int)
    pagination = Guoke.objects.paginate(page=page, per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource': [i.to_json() for i in pagination.items],
        'has_next': pagination.has_next,
        'current_page': page,
        'total_pages': pagination.pages
    })


@main.route('/api/zhihu/article', methods=['GET'])
def zhihu():
    page = request.args.get('page', 1, type=int)
    pagination = Zhihu.objects.paginate(page=page, per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource': [i.to_json() for i in pagination.items],
        'has_next': pagination.has_next,
        'current_page': page,
        'total_pages': pagination.pages
    })


@main.route('/api/douban/search', methods=['GET'])
def douban_search():
    page = request.args.get('page', 1, type=int)
    query_words = request.args.get('query', '')
    res = client.search(
        index="douban",
        body={
            "query": {
                "multi_match": {
                    "query": query_words,
                    "fields": ["source_from", "title", "content"]
                }
            },
            "from": (page - 1) * current_app.config['PER_PAGE'],
            "size": current_app.config['PER_PAGE'],
        }
    )
    result = []
    total = res['hits']['total']
    for hit in res['hits']['hits']:
        result.append(hit["_source"])
    return jsonify({
        'article_resource': result,
        'has_next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages': int(ceil(total / float(current_app.config['PER_PAGE'])))

    })


@main.route('/api/guoke/search', methods=['GET'])
def guoke_search():
    page = request.args.get('page', 1, type=int)
    query_words = request.args.get('query', '')
    res = client.search(
        index="guoke",
        body={
            "query": {
                "multi_match": {
                    "query": query_words,
                    "fields": ["source_from", "title", "content"]
                }
            },
            "from": (page - 1) * current_app.config['PER_PAGE'],
            "size": current_app.config['PER_PAGE'],
        }
    )
    result = []
    total = res['hits']['total']
    for hit in res['hits']['hits']:
        result.append(hit["_source"])
    return jsonify({
        'article_resource': result,
        'has_next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages': int(ceil(total / float(current_app.config['PER_PAGE'])))

    })


@main.route('/api/zhihu/search', methods=['GET'])
def zhihu_search():
    page = request.args.get('page', 1, type=int)
    query_words = request.args.get('query', '')
    res = client.search(
        index="zhihu",
        body={
            "query": {
                "multi_match": {
                    "query": query_words,
                    "fields": ["source_from", "title", "content"]
                }
            },
            "from": (page - 1) * current_app.config['PER_PAGE'],
            "size": current_app.config['PER_PAGE'],
        }
    )
    result = []
    total = res['hits']['total']
    for hit in res['hits']['hits']:
        result.append(hit["_source"])
    return jsonify({
        'article_resource': result,
        'has_next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages': int(ceil(total / float(current_app.config['PER_PAGE'])))

    })


@main.route('/api/all/search', methods=['GET'])
def all_search():
    page = request.args.get('page', 1, type=int)
    query_words = request.args.get('query', '')
    res = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": query_words,
                    "fields": ["source_from", "title", "content"]
                }
            },
            "from": (page - 1) * current_app.config['PER_PAGE'],
            "size": current_app.config['PER_PAGE'],
        }
    )
    result = []
    total = res['hits']['total']
    for hit in res['hits']['hits']:
        result.append(hit["_source"])
    return jsonify({
        'article_resource': result,
        'has_next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages': int(ceil(total / float(current_app.config['PER_PAGE'])))

    })

@main.route('/api/user/favor',methods=['GET','PUT'])
@basic_auth.login_required
def user_favor():
    user = g.current_user
    pass