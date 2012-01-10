#!/usr/bin/env python
# encoding: utf-8
import sys
import sqlite3
reload(sys) 
sys.setdefaultencoding("utf-8")
sys.path.append("../pylibrary")
#sys.path.append("../pylibrary")
sys.path.append('/Users/jean-philippecointet/Desktop/cortext/manager/scripts/pylibrary')


import fonctions

"""
library.py

Created by Jean-Philippe Cointet on 2011-12-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

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
# print pattern.search("samedi 15 Janvier 2006sdqklm")
# print pattern.search("samedi 15 août 2006sdqklm")
# print pattern.search("samedi 15 août 2006 sdqklm").groups()
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


def extracturls_corpus(con):
	cur=con.execute("select urlid,domain from urlcorpus ")
	res=cur.fetchall()
	pages = {}
	for result in res:
		pages[result[0]]=result[1]
	return pages
	
def extractlinks(con,urls_corpus):
	cur=con.execute("select fromid,toid from link ")
	links=cur.fetchall()
	num_links=0
	link_list={}
	for link in links:
		(fromid,toid)=link
		if fromid!=toid:
			if fromid in urls_corpus and toid in urls_corpus:
				link_list.setdefault(fromid,[]).append(toid)
				num_links+=1
	print len(link_list),'total unique links'
	return link_list


def extractdata(con):
	fields =con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
	cur=con.execute("SELECT * FROM  urlcorpus")
	print cur.description
	fields = [tuple[0] for tuple in cur.description]
	print fields
	questions=','.join(['?'] * (len(fields)))
	fields_txt=','.join(fields)
	#print "select  "+questions +" from urlcorpus ",fields
	#cur=con.execute("select  "+questions +" from urlcorpus ",fields)
	cur=con.execute("select  "+fields_txt +" from urlcorpus ")
	res=cur.fetchall()
	pages = {}
	salient_fields=[ 'url', 'text_summary','title', 'domain', 'date_date']
	names={}
	names['url']='ISIT9'
	names['domain']='ISIJOURNAL'
	names['title']='ISItitle'
	names['text_summary']='ISIabstract'
	
	notices={}
	for result in res:
		id=result[0]
		notice={}
		for field,y in zip(fields,result):
			if field in salient_fields:
				notice[names.get(field,field)]=[[y]]
		notice['ISIpubdate']=[['1']]
		notices[id]=notice
	return notices			
	

def exportcrawl2resolu(db_crawl,query,result_path):
	db_resolu=db_crawl[:-9]+'solved.db'
	print 'db_resolu',db_resolu
	print 'db_crawl',db_crawl
	con_crawl=sqlite3.connect(db_crawl)
	con_resolu=sqlite3.connect(db_resolu)
	
	urls_corpus=extracturls_corpus(con_crawl)
	dict_links=extractlinks(con_crawl,urls_corpus)
	
	notices =extractdata(con_crawl)
	
	for notice_id,notice in notices.iteritems():
		if notice_id in dict_links:
			print dict_links[notice_id]
			notices[notice_id]['ISICitedRef']=map(lambda x: notices[x]['ISIT9'][0],dict_links[notice_id])
			notices[notice_id]['ISIRef']=map(lambda x: notices[x]['ISIT9'][0],[notice_id])
			notices[notice_id]['ISICRJourn']=map(lambda x: notices[x]['ISIJOURNAL'][0],dict_links[notice_id])
	#print notices
	build_se=True
	
	dico_tag={}
	dico_tag['url']='ISIT9'
	dico_tag['domain']='ISIJOURNAL'
	dico_tag['title']='ISITITLE'
	dico_tag['text_summary']='ISIABSTRACT'
	
	nb_notice_afficher=10
	mapping_complet = fonctions.afficher_notices(notices,dico_tag,nb_notice_afficher)
	
	if build_se==True and len(notices.keys())>0:
			#sys.path.append("../parser_science")
			try:
				sys.path.append('../parser_science')
			except:
				pass
			try:
				sys.path.append('/Users/jean-philippecointet/Desktop/cortext/manager/scripts/parser_science')
			except:
				pass
			try:
				sys.path.append('../../parser_science')
			except:
				pass
		
			import whoosh_init
			print 'SE built there:',result_path
			# if corpus_type=='factiva':
			# 				tags = ['accessionNo','reference','baseLanguage','byline','copyright','sourceName','wordCount','headline','leadParagraph','tailParagraphs','pages','publicationDate','region','newsSubject','company','industry']
			# 				mapping_complet={}
			# 				for tag in tags:
			# 					mapping_complet[tag]=tag
			# 					
			# 			elif corpus_type=='xmlpubmed':
			# 				tags = ['PMID','PubDate','DateCreated','DateCompleted','ISSN','Volume','Issue','ArticleTitle','Title','Author','ISOAbbreviation','ArticleTitle','MedlinePgn','Language','PublicationType','Grant','MedlineJournalInfo','ISSNLinking','Chemical','NameOfSubstance',\
			# 	'CitationSubset','RefSource','MeshHeading','Abstract','Affiliation','CommentsCorrections',	'Author_name','Author_firstname','MeshHeading_Description','ISIpubdate','PMID','Journal']
			# 				mapping_complet={}
			# 				for tag in tags:
			# 					mapping_complet[tag]=tag
			# 			
			ix=whoosh_init.instantiate(result_path,mapping_complet,'isi',True,query)
			whoosh_init.seed_se(ix,notices,'isi')
	fonctions.insert_notices(db_resolu,True,notices,dico_tag,mapping_complet,corpus_name=query,output_type='reseaulu')
