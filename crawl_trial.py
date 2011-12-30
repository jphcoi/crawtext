#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
reload(sys) 
sys.setdefaultencoding("utf-8")
import seachengine2
import warnings
from library import *

warnings.filterwarnings("ignore")

global pages
pages={}

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
	

inlinks_min=parameters.get('inlinks_min',1)
depth=parameters.get('depth',10)
query=parameters.get('query','You really should enter a query, otherwise...')

 
#path = 'data/algsang'

#http://www.scroogle.org/cgi-bin/scraper.htm #feed a path with links grabbed from scroogle!
#crawler parameters

#inlinks_min=1
#depth=7

from  pattern import web

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
		if not check_forbidden(new_url) and not new_url in pages:
			pages[new_url]=inlinks_min

print 'pages init',len(pages)
print 'pages',pages
query='algues vertes AND sangliers'
#query='biofuel'
try:
	os.mkdir('ouput')
except:
	pass
crawler=seachengine2.crawler('ouput/'+query+'_crawl.db')
try:
  crawler.createindextables()
except:
  print "tables already exist, good"

crawler.crawl(pages,query=query,inlinks=inlinks_min,depth=depth)
