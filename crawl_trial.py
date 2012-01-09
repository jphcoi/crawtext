#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
reload(sys) 
sys.setdefaultencoding("utf-8")
import seachengine2
import warnings
from library import *
from  pattern import web

warnings.filterwarnings("ignore")

global pages
pages={}
global pattern_date_fr
# try:
# 	os.mkdir('data')
# except:
# 	pass
		
import yaml
try:
	user_parameters=sys.argv[1]
except:
	user_parameters='crawl_parameters.yml'

parameters = yaml.load('\n'.join(open(user_parameters,'r').readlines()))

try:
	path = parameters['path']
except:
	print 'invalid parameters file'
	path=parameters['corpus_file']

inlinks_min=parameters.get('inlinks_min',1)
depth=parameters.get('depth',10)
query=parameters.get('query','You really should enter a query, otherwise...')
result_path=parameters.get('result_path','ouput')
print 'query',query
#crawler parameters
 
#path = 'data/algsang'
#inlinks_min=1
#depth=7


dirList=os.listdir(path)
for fname in dirList:
	pagelist =os.path.join(path,fname)
	print 'pagelist',pagelist
	url=web.URL(pagelist)
	chaine=url.download(cached=False)
	new_urls = map(lambda x: url_uniformer(x.split('">')[0]),web.find_urls(chaine, unique=True))
	if 'Google Search' in pagelist:
		 new_urls = map(lambda x:x.split("&amp;")[0],new_urls)
	for new_url in new_urls[:]:
		if not check_forbidden((new_url,'')) and not new_url in pages:
			pages[new_url]=inlinks_min

print 'pages init',len(pages)
print 'pages',pages

db_name=os.path.join(result_path,query+'_crawl.db')


# # try:	
# # 	os.mkdir(result_path)
# # 	os.remove(os.path.join(result_path,query+'_crawl.db'))
# # 	print 'deleted',result_path+query+'_crawl.db'
# # except:
# # 	pass

# # crawler=seachengine2.crawler(db_name)
# # try:
# #   crawler.createindextables()
# # except:
# #   print "tables already exist, good"
# 
# crawler.crawl(pages,query=query,inlinks=inlinks_min,depth=depth)
exportcrawl2resolu(db_name,query,result_path)