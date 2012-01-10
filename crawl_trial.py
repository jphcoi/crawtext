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
print 'parameters',parameters
try:
	path = parameters['path']
except:
	print 'invalid parameters file'
	path=parameters['corpus_file']

	
print 'path',path
inlinks_min=int(parameters.get('inlinks_min',1))
depth=int(parameters.get('depth',10))
query=parameters.get('query','You really should enter a query, otherwise...')
result_path=parameters.get('result_path','ouput')
print 'query',query
max_pages_number=int(parameters.get('max_pages_number',10000))
if max_pages_number == 999999:
	pass
else:
	max_pages_number=min(max_pages_number,100000)

import sys, zipfile, os, os.path

def unzip_file_into_dir(file, dir):
	try:
		os.mkdir(dir, 0777)
	except:
		pass
	zfobj = zipfile.ZipFile(file)
	for name in zfobj.namelist():
		if name.endswith('/'):
			try:
				os.mkdir(os.path.join(dir, name))
			except:
				pass
		else:
			outfile = open(os.path.join(dir, name), 'wb')
			outfile.write(zfobj.read(name))
			outfile.close()

if path[-4:]=='.zip':
		print 'on dezip' + path
		corpus_out = '/'.join(path.split('/')[:-1]) + '/'+query
		print corpus_out
		unzip_file_into_dir(path,corpus_out)
		path=corpus_out

print 'path',path
#crawler parameters
 
#path = 'data/algsang'
#inlinks_min=1
#depth=7


dirList=os.listdir(path)
for fname in dirList:
	pagelist =os.path.join(path,fname)
	print 'pagelist',pagelist
	try:
		url=web.URL(pagelist)
		chaine=url.download(cached=False)
		new_urls = map(lambda x: url_uniformer(x.split('">')[0]),web.find_urls(chaine, unique=True))
		if 'Google Search' in pagelist:
			 new_urls = map(lambda x:x.split("&amp;")[0],new_urls)
		for new_url in new_urls[:]:
			if not check_forbidden((new_url,'')) and not new_url in pages:
				pages[new_url]=inlinks_min
	except:
		pass
print 'pages init',len(pages)
print 'pages',pages

db_name=os.path.join(result_path,query+'_crawl.db')


try:	
	os.mkdir(result_path)
	os.remove(os.path.join(result_path,query+'_crawl.db'))
	print 'deleted',result_path+query+'_crawl.db'
except:
	pass

crawler=seachengine2.crawler(db_name)
try:
  crawler.createindextables()
except:
  print "tables already exist, good"

crawler.crawl(pages,query=query,inlinks=inlinks_min,depth=depth,max_pages_number=max_pages_number)
exportcrawl2resolu(db_name,query,result_path)