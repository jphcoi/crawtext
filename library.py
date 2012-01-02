#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys) 
sys.setdefaultencoding("utf-8")

"""
library.py

Created by Jean-Philippe Cointet on 2011-12-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import re
forbidden_sites=map(lambda x: x[:-1],open('forbidden_sites.txt','r').readlines())
print 'forbidden_sites:	',forbidden_sites
forbidden_linktext=map(lambda x: (x[:-1]),open('forbidden_linktext.txt','r').readlines())
print 'forbidden_linktext:	',forbidden_linktext

dateregexp=re.compile('(\d{4})-(\d{2})-(\d{2})')
forbiden_site='('+')|('.join(forbidden_sites)+')'
#forbiden_site=r('|'.join(forbidden_sites))
machin='|'.join(forbidden_sites).replace('?','\?')#.replace('/',"\/")
#forbiden_site=r"www.wikio.fr|twitter.com/|kelkoo.fr/|partner.googleadservices.com|alvinet.com|http://fr.wordpress.com|&q=related:|?q=related:|https://webcache.googleusercontent.co|http://webcache.googleusercontent.com|https://accounts.google.com/ServiceLogin?|http://www.google.com|https://plus.google.com/|http://t1.gstatic.com/|http://t0.gstatic.com/|accounts.google.com/|http://maps.google.com|support.google.com|?action=illicite|&action=illicite|.google.com|.gstatic.co"
#forbiden_site=r"&q=related:|\?qwww.wikio.fr|twitter.com/|kelkoo.fr/|partner.googleadservices.com|alvinet.com|http://fr.w"
forbiden_site=r"%s" % machin
regexp_forbiden_site=re.compile(forbiden_site)
machintxt='|'.join(forbidden_linktext).replace('?','\?')
forbiden_txt=r"%s" % machintxt
regexp_forbiden_txt=re.compile(forbiden_txt)
# print 'voir les 30 commentaires', regexp_forbiden_txt.search('voir les 30 commentaires')
# print 'afficher les 30 commentaires', regexp_forbiden_txt.search('afficher les 30 commentaires')
# print 'si vous affichezs les 30 commentaires', regexp_forbiden_txt.search('affichezs les 30 commentaires')
# print 'imprimera', regexp_forbiden_txt.search('imprimera')


pattern = re.compile(r'(\d|\d\d)\s(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s(\d{4})',re.I)
print pattern.search("samedi 15 Janvier 2006sdqklm")
print pattern.search("samedi 15 août 2006sdqklm")
print pattern.search("samedi 15 août 2006 sdqklm").groups()
def check_forbidden(urle):
	(url,urltxt)=urle
	
	#for forbid in forbidden_sites:
		#if forbid in url:
	if not regexp_forbiden_site.search(url)==None:
			print url, ' declined (fordbideen list)'
			return True
	#for forbidtxt in forbidden_linktext:
	#	if forbidtxt==urltxt.lower():
	if not regexp_forbiden_txt.search(urltxt.lower())==None:
			print urltxt, ' declined (fordbideentxt list)'
			return True
	return False

def unique(list):
	list_clean = []
	for item in list:
		if not item in list_clean:
			list_clean.append(item)
	return list_clean

def url_uniformer(url):
	if url[0:4]=='http':
		pass
	else:
		url = 'http://' + url
	url = url.split('#')[0]#get rid of js parameters
	return url
	

class webpage:
	url=None
	url_redirected=None
	html=None
	html_summary=None
	text_summary=None
	domain=None
	query_result=None
	url_feed=None
	path=None
	links=None
	charset=None
	title=None
