# -*- coding: utf-8 -*-
from datetime import datetime
from math import ceil

from flask import request, current_app, jsonify, render_template, g

from app.utils.pagination import Paginate
from . import main
from .. import client
from ..auth.authentication import basic_auth
from ..models import Douban, Guoke, Zhihu, ItemFavor
from ..responses import suc_response, not_found


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@main.route('/query', methods=['GET', 'POST'])
def query():
    keywords = request.args.get('keywords')
    return render_template('search.html', keywords=keywords)


@main.route('/api/hot/article', methods=['GET'])
def hot():
    if ItemFavor.objects.count() < 10:
        return jsonify({
            'article_resource': [i.item.to_json() for i in ItemFavor.objects]
        })
    sort_list = sorted(ItemFavor.objects,
                       key=lambda i: len(i.favor_user) * 1000 / ((datetime.utcnow() - i.item.add_time).seconds / 3600.0 + 2) ** 1.2,
                       reverse=True)
    return jsonify({
        'article_resource': [i.item.to_json() for i in sort_list[:10]]
    })


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


@main.route('/api/user/all-favor', methods=['GET'])
@basic_auth.login_required
def user_favor():
    page = request.args.get('page', 1, type=int)
    user = g.current_user
    pagination = Paginate(iterable=user.favor, current_page=page, per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource': [i.to_json() for i in pagination.items],
        'has_next': pagination.has_next,
        'current_page': page,
        'total_pages': pagination.pages
    })


@main.route('/api/user/favor/<string:data_id>', methods=['GET', 'PUT', 'DELETE'])
@basic_auth.login_required
def data_favor(data_id):
    user = g.current_user
    all_item = [Zhihu, Douban, Guoke]
    item = None
    for a in all_item:
        item = a.objects.filter(data_id=data_id).first()
        if item:
            break
    if not item:
        return not_found('not found the data')
    item_favor = ItemFavor.objects.filter(item=item).first()

    if request.method == 'GET':
        favor = False
        if not item_favor:
            return jsonify({
                'favor': favor,
                'count': len(item_favor.favor_user) if item_favor else 0
            })

        for u in item_favor.favor_user:
            if user == u:
                favor = True
        item_favor.reload()
        return jsonify({
            'favor': favor,
            'count': len(item_favor.favor_user) if item_favor else 0
        })
    elif request.method == 'PUT':
        for i in user.favor:
            if item == i:
                return suc_response('you  already have the favor')
        user.favor.append(item)
        user.save()
        if not item_favor:
            item_favor = ItemFavor(item=item)
            item_favor.save()
        item_favor.favor_user.append(user)
        item_favor.save()
        return suc_response('add the favor successfully')
    elif request.method == 'DELETE':
        if not item_favor:
            return suc_response('you have already remove the data')
        if user not in item_favor.favor_user and item_favor.item not in user.favor:
            return suc_response('you have already remove the data')
        item_favor.favor_user.remove(user)
        item_favor.save()
        user.favor.remove(item_favor.item)
        user.save()
        return suc_response('remove sucessfully')
