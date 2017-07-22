# Daily

![](https://img.shields.io/badge/python-2.7-brightgreen.svg)
![](https://img.shields.io/badge/Flask-0.12-yellowgreen.svg)
![](https://img.shields.io/badge/MongoDB-3.4.3-orange.svg)
![](https://img.shields.io/badge/elasticsearch-5.4.0-green.svg)
![](https://img.shields.io/badge/Bootstrap-3-orange.svg)
![](https://img.shields.io/badge/jquery-1.9-brightgreen.svg)
### work with [search_spider](https://github.com/william-tu/search_spider)


## 简介
Daily是一款文章浏览型应用，旨在提供优质的文章导航。
目前爬取的文章有知乎豆瓣果壳的文章

通过[search_spider](https://github.com/william-tu/search_spider)爬取文章部分信息保存至mongodb和elasticsearch数据库，Flask提供接口,bootstrap,jquery进行数据的展示

## start
### 一：

	$ virtualenv venv // 建立虚拟环境
	$ source venv/bin/activate // 激活虚拟环境
	$ pip install -r requirements //导入依赖
	$ touch config.py // 新建配置文件
例如
config.py

	# -*- coding: utf-8 -*-
	class Config:
	    MONGODB_HOST = 'localhost' 
	    MONGODB_PORT = 27017 # mongodb端口号 默认是27017
	    MONGODB_DB = 'spider' # mongodb数据库名
	    PER_PAGE = 10 # 数据接口每次返回的数据数量
	    ELASTICSEARCH_URL = 'http://localhost:9200/' # elastcsearch数据库 url 此为默认
		
	
	class DevelopmentConfig(Config):
	    DEBUG = True
	
	config = {'default': DevelopmentConfig}

### 二：配置数据库
1. 配置mongodb(这里不赘述)
2. 配置elasticsearch

>这里elasticsearch版本是5.4.0 , elasticsearch开源[地址](https://github.com/elastic/elasticsearch)

3. 为elasticsearch配置**ik**分词器插件

 elasticsearch-analysis-ik [地址](https://github.com/medcl/elasticsearch-analysis-ik),注意和elasticsearch版本对应。

### 三：导入数据
	(venv) $ cd app
	(venv) $ python es_models
	
然后将dbs.json导入数据库，注意数据库的结构,详情查看model

