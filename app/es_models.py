# -*- coding: utf-8 -*-
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])


class DoubanType(DocType):
	id = Keyword()
	title = Text(analyzer='ik_max_word')
	content = Text(analyzer='ik_max_word')
	message_url = Keyword()
	image_url = Keyword()
	add_time = Date()
	source_from = Text(analyzer='ik_max_word')

	class Meta:
		index = 'douban'
		doc_type = 'article'

class GuokeType(DocType):
	id = Keyword()
	title = Text(analyzer='ik_max_word')
	content = Text(analyzer='ik_max_word')
	message_url = Keyword()
	image_url = Keyword()
	add_time = Date()
	source_from = Text(analyzer='ik_max_word')

	class Meta:
		index = 'guoke'
		doc_type = 'article'


if __name__=='__main__':
	DoubanType.init()
	GuokeType.init()