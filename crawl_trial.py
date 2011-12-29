#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
reload(sys) 
sys.setdefaultencoding("utf-8")
import seachengine2
import warnings
from library import *

warnings.filterwarnings("ignore")

#pagelist=["http://www.bretagne-environnement.org/Mer-littoral/Les-menaces/Marees-vertes/La-proliferation-des-algues-vertes","http://www.slate.fr/tribune/46101/algues-vertes"]
# pagelist=["http://www.bretagne-environnement.org/Mer-littoral/Les-menaces/Marees-vertes/La-proliferation-des-algues-vertes"]
# pagelist=["http://www.poilagratter.net/?p=3261","http://danieljaglinedjexreveur.over-blog.com/article-algues-vertes-faire-du-desastre-un-atout-sans-omettre-de-les-eradiquer-a-terme-90027126.html","http://marino1.over-blog.com/article-les-algues-vertes-tueuses-89587099.html","http://npa29quimper.over-blog.fr/article-debat-algues-vertes-a-brest-89672301.html","http://lautregrenelledelamer.over-blog.com/article-algues-vertes-tous-les-acteurs-reunis-ce-samedi-a-fouesnant-of-89583483.html"]
# pagelist=["http://www.earthtechling.com/2011/12/u-s-biofuels-policy-a-fail-in-new-study/","http://www.globalwarming.org/2011/11/30/do-biofuel-mandates-and-subsidies-imperil-food-security/","http://www.renewableenergyworld.com/rea/news/article/2011/11/advanced-biofuels-taking-off-use-of-non-food-bio-based-jet-fuel-climbing"]
# #pagelist=[]
# pagelist=["http://www.globalwarming.org/2011/11/30/do-biofuel-mandates-and-subsidies-imperil-food-security/","http://www.renewableenergyworld.com/rea/news/article/2011/11/advanced-biofuels-taking-off-use-of-non-food-bio-based-jet-fuel-climbing","http://blogs.physicstoday.org/newspicks/2011/09/microwave-wast-to-get-biofuel.html","http://africanpress.me/2011/11/13/diversion-of-maize-to-produce-biofuel-will-continue-to-send-food-prices-aflutter-2/"]
# pagelist_list=['data/alguesvertes/alguesvertes.htm','data/alguesvertes/alguesvertes2.htm','data/alguesvertes/alguesvertes3.htm','data/alguesvertes/alguesvertes4.htm','data/alguesvertes/alguesvertes5.htm']
global pages
pages={}

try:
	os.mkdir('data')
except:
	pass
	
path = 'data/alguesverteslight2'
#http://www.scroogle.org/cgi-bin/scraper.htm #feed a path with links grabbed from scroogle!

#crawler parameters
inlinks_min=1
depth=7

from  pattern import web

dirList=os.listdir(path)
for fname in dirList:
	pagelist =os.path.join(path,fname)
	print pagelist
	url=web.URL(pagelist)
	chaine=url.download(cached=False)
	new_urls = map(lambda x: url_uniformer(x.split('">')[0]),web.find_urls(chaine, unique=True))
	for new_url in new_urls:
		if not check_forbidden(new_url) and not new_url in pages:
			pages[new_url]=inlinks_min

print 'pages init',len(pages)

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
