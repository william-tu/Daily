# -*- coding: utf-8 -*-
from flask import request,current_app,jsonify
from . import main
from ..models import Douban,Guoke
from .. import client


from math import ceil


@main.route('/api/douban/article',methods=['GET'])
def douban():
    page = request.args.get('page',1,type=int)
    pagination = Douban.objects.paginate(page=page,per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource':[ i.to_json() for i in pagination.items],
        'next': pagination.has_next,
        'pages':pagination.pages
    })

@main.route('/api/guoke/article',methods=['GET'])
def guoke():
    page = request.args.get('page',1,type=int)
    pagination = Guoke.objects.paginate(page=page,per_page=current_app.config['PER_PAGE'])
    return jsonify({
        'article_resource':[ i.to_json() for i in pagination.items],
        'next': pagination.has_next,
        'current_page': page,
        'total_pages':pagination.pages
    })

@main.route('/api/douban/search',methods=['GET'])
def douban_search():
    page = request.args.get('page', 1,type=int)
    query_words = request.args.get('query','')
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
        'next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages':int(ceil(total/float(current_app.config['PER_PAGE'])))

    })

@main.route('/api/guoke/search',methods=['GET'])
def guoke_search():
    page = request.args.get('page', 1,type=int)
    query_words = request.args.get('query','')
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
        'next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages':int(ceil(total/float(current_app.config['PER_PAGE'])))

    })

@main.route('/api/zhihu_daily/search',methods=['GET'])
def zhihu_daily_search():
    page = request.args.get('page', 1,type=int)
    query_words = request.args.get('query','')
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
        'next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages':int(ceil(total/float(current_app.config['PER_PAGE'])))

    })

@main.route('/api/all/search',methods=['GET'])
def all_search():
    page = request.args.get('page', 1,type=int)
    query_words = request.args.get('query','')
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
        'next': page * current_app.config['PER_PAGE'] < total,
        'current_page': page,
        'total_pages':int(ceil(total/float(current_app.config['PER_PAGE'])))

    })


