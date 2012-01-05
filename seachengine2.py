#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
reload(sys) 
sys.setdefaultencoding("utf-8")
import sqlite3
from pyparsing import *
from random import choice
from library import *
import multiprocessing
import socket
#from lxml import html
#from lxml.html.clean import clean_html
sys.path.append("decruft")
import decruft
import urllib2
import feedparser
import pattern
from  pattern import web
from BeautifulSoup import BeautifulSoup as parser
from urlparse import urljoin
import warnings
import chardet
import time
import re
warnings.filterwarnings("ignore")
import hashlib

socket.setdefaulttimeout(30)
pattern_date_fr = re.compile(r'(\d|\d\d)\s(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s(\d{4})',re.I)


user_agents = [
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
	'Opera/9.25 (Windows NT 5.1; U; en)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
	'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
	'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
	'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]



# def rss_analyze(rssfeed_url):
# 	#print 'rss url',rssfeed_url				
# 	try:
# 		d = feedparser.parse(rssfeed_url)
# 	# print 'title:',d.feed.title
# 	# print 'link:',d.feed.link
# 	# print 'description:',d.feed.description
# 	# print 'd.feed.date',d.feed.date
# 	# print 'd.feed.date_parsed',d.feed.date_parsed
# 		for key in d.entries[0]:
# 			print key, ' : ',d.entries[0][key]
# 	except:
# 		pass
# 	
# 	
# 	
# def detect_feeds_in_HTML(input_stream):
#     """ examines an open text stream with HTML for referenced feeds.
# 
#     This is achieved by detecting all ``link`` tags that reference a feed in HTML.
# 
#     :param input_stream: an arbitrary opened input stream that has a :func:`read` method.
#     :type input_stream: an input stream (e.g. open file or URL)
#     :return: a list of tuples ``(url, feed_type)``
#     :rtype: ``list(tuple(str, str))``
#     """
#     # check if really an input stream
#     if not hasattr(input_stream, "read"):
#         raise TypeError("An opened input *stream* should be given, was %s instead!" % type(input_stream))
#     result = []
#     # get the textual data (the HTML) from the input stream
#     html = parser(input_stream.read())
#     # find all links that have an "alternate" attribute
#     feed_urls = html.findAll("link", rel="alternate")
#     # extract URL and type
#     for feed_link in feed_urls:
#         url = feed_link.get("href", None)
#         # if a valid URL is there
#         if url:
#             result.append(url)
#     return result


# Create a list of words to ignore
	


def check_query(query,text):
	if ' AND ' in query:
		queries=map(lambda x:x.lower(),query.split(' AND '))
	else:
		queries=[query]
	textl=text.lower()
	for query in queries:
		if not query in textl:
			return False
	return True


def check_page_against_query(html,title,query):#check actual content of the page against the query
	if 1:#check_query(query,str(html)):
		try:
			html_summary=decruft.Document(html).summary()
			text_summary=web.plaintext(html_summary, keep=[], replace=web.blocks, linebreaks=2, indentation=False)
		except:
			print 'cant use generic tools to get a summary'
			html_summary=htm
			text_summary = str(html)
		return check_query(query,title+'\n&&&&&&&&&&&&&\n'+text_summary),text_summary,html_summary
	else:
		return False,'text_summary','html_summary'#useless to compute the text_summary...
	
def looking4charset(metas):
	for meta in metas:
		meta=str(meta)
		if 'charset=' in meta:
			return meta.split("charset=")[1].split('"')[0]
	return None


class Webpage:
	url=None
	url_redirected=None
	html=None
	html_summary=None
	text_summary=None
	domain=None
	query_result=False
	url_feed=None
	path=None
	links=None
	charset=None
	title=None
	opened=0
	successful_open=False
	md5=''
	date=''
	url_redirected=None
	mimetype=None
	links_whole=None
	def display_page(self):
		
		#print 'page url: ',self.url
		#print 'text_summary',self.text_summary
		print 'html_summary',self.html_summary
		#print 'links: ',self.links
		#print 'path: ',self.path
		#print 'charset: ',self.charset
		#print 'title:',self.title
		#print 'md5',self.md5
		
#		(urlid,unicode(webpage.url),unicode(webpage.text_summary).replace("'","''"),unicode(webpage.html_summary).replace("'","''"),u
		
def extract_data(package):
	(page,query)=package
	
	#print page
	new_webpage=Webpage()
	new_webpage.url=page
	try:
		url=web.URL(page)
		mimetype=url.mimetype
		new_webpage.mimetype=mimetype
		if mimetype=='text/html':#only load Webpages!!!
			domain = url.domain# u'domain.com'
			url_feed=''
			redirected_page=url.redirect# Actual URL after redirection, or None.		
			path= url.path# [u'path']
			# different options to open a webpage
			html=url.download(user_agent=choice(user_agents),cached=False)
			#html = urllib2.urlopen(page).read()
		else:
			#print 'bad mimetype',mimetype,page
			new_webpage.successful_open=True
	except:
		#print "*** Could not open page: %s" % page
		new_webpage.successful_open=False
	try:
		if check_query(query,str(html)):#on s'assure d'abord que ça roule pour le full html
			new_webpage.successful_open=True
			
			dom = web.Document(html)
			try:
				title = dom.by_tag('title')[0]		
				title = repr(web.plaintext(title.content))
			except:
				title=''
		
		
		
			#two methods for charset detection:
			charset=None
			# option to detect page encoding from dom structure => does not seem to work utf-8 systematically retrieved...???
			# try:
			# 	metas=dom.by_tag('meta')
			# 	charset=looking4charset(metas)
			# 	print 'charset',charset, 'in page',page
			# except:
			# 	charset=None
			#
		
			# chardet library use
			# if charset==None: 
			# 	encoding = chardet.detect(html)
			# 	html=html.decode(encoding['encoding'])
			# else:
			# 	html=html.decode(charset)

			query_result,text_summary,html_summary=check_page_against_query(html,title,query)
			# charset guess can be used to decode results
			# if charset==None:
			# 	encoding = chardet.detect(html)
			# 	html=html.decode(encoding['encoding'])
			# else:
			# 	html=html.decode(charset)


			#save in a repertory output textual summaries
			#fileout=open('temp/'+page[7:20]+'.htm','w')
			#print 'temp/'+page+'.htm'
			#fileout.write(html_summary)
			#fileout.close()

			#if query_result:
				# dom = web.Document(html_summary)
				# try:
				# 	date = dom.by_tag('date')[0]		
				# 	date = repr(plaintext(date.content))
				# except:
				# 	date=''
				# print '######date',date
			dateregexp=re.compile(r'(\d{4})-|\\(\d{2})-|\\(\d{2})')

			date=''
			if not redirected_page==None:
				print 'plus redirection: ',redirected_page
				try:
					date = dateregexp.search(redirected_page).groups()
					new_webpage.date='-'.join(date)
				except:
					pass
			else:
				try:
					date = dateregexp.search(page).groups()
					new_webpage.date='-'.join(date)
				except:
					pass
			#print '#############date',date
			
		
			if date=='':
				date_txt=pattern_date_fr.search(str(text_summary))		
				if not date_txt==None:
					date=date_txt.groups()
					new_webpage.date='-'.join(date)
			#date_txt=pattern_date_fr.search("Samedi 6 août 2011606/08/Août/201120:29")
			if query_result:
				print 'page: ', new_webpage.url,' with title: ', title,' and date',new_webpage.date ,'was assessed as ',query_result
		
			#print 'date_txt'
			#print 'date_txt:',str(date_txt)
			#feed webpage details with informations
			new_webpage.url_redirected=redirected_page
			new_webpage.html=html
			new_webpage.html_summary=html_summary
			new_webpage.text_summary=text_summary
			new_webpage.domain=domain
			new_webpage.query_result=query_result
			new_webpage.url_feed=url_feed
			new_webpage.path=path
			new_webpage.charset=charset
			new_webpage.title=title
			new_webpage.opened=new_webpage.opened+1
			new_webpage.md5=hashlib.sha224(text_summary).hexdigest()
		
			#new_webpage.display_page()
			#new_webpage.links=None
		else:
			#the query is not even in the raw html
			new_webpage.successful_open=True
			new_webpage.query_result=False
	except:
		#print "*** Could not extract data from %s" % page
		pass
	return new_webpage



# Extract the text from an HTML page (no tags)
def gettextonly(soup):
    v=soup.string
    if v==None:
        c=soup.contents
        resulttext=''
        for t in c:
          subtext=gettextonly(t)
          resulttext+=subtext+'\n'
        return resulttext
    else:
        return v.strip()

def find_url(domain,page,text,only_out=True):
	soup=parser(text)
	links=soup('a')
	#print 'links',links
	links_final=[]
	#print 'domain',domain
	page_root = page.replace('http://','').replace('www','').split('/')[0]
	for link in links:	
		try:
			if ('href' in dict(link.attrs)):
				url=urljoin(page,link['href'])
				if url.find("'")!=-1: continue
				url=url.split('#')[0]	 # remove location portion
				if url[0:4]=='http':
					linkText=gettextonly(link)
					if only_out:
						link_root=link['href'].replace('http://','').replace('www','').split('/')[0]
						if link_root!=page_root:
							links_final.append((url_uniformer(url),linkText))
					else:
						links_final.append((url_uniformer(url),linkText))
		except:
			pass
	return links_final

	
def extract_links(webpage):
	#(page,html,querycheck,rssfeed_url,text,redirected_page,html_summary,domain,webpage)=data
	citations=[]
	citations_whole=[]
	linktxtfile=open('linktext','a')
	page_old=webpage.url
	if not webpage.url_redirected==None: 
		webpage.url=webpage.url_redirected
	if webpage.query_result:
		#links=unique(web.find_urls(html_summary, unique=True))
		links=unique(find_url(webpage.domain,webpage.url,webpage.html_summary,only_out=False))#on chercher les liens uniquement dans le contenu pertinent
		links_whole=unique(find_url(webpage.domain,webpage.url,webpage.html,only_out=False))#on chercher les liens uniquement dans le contenu pertinent
		for linke in links:#in find_url(page,html):#web.find_urls(text, unique=True):
			if not check_forbidden(linke):
					link,linkText=linke
					linktxtfile.write(linkText+'\n')
					if not link[0:4]=='http':
						link = 'http//'+link
					else:
						citations.append(link)
		for linke in links_whole:#in find_url(page,html):#web.find_urls(text, unique=True):
			if not check_forbidden(linke):
					link,linkText=linke
					linktxtfile.write(linkText+'\n')
					if not link[0:4]=='http':
						link = 'http//'+link
					else:
						citations_whole.append(link)


		print 'investigating a new page ', webpage.url, ' with ', len(citations), ' citation links'
		soup=''
		webpage.links = citations[:]
		webpage.links_whole = citations_whole[:]
		#return (page_old,soup,html,link_total,text,redirected_page,domain,webpage)
	else:
		webpage.links='link_total'
		webpage.links_whole='link_total'
		#return (page_old,'soup','html','link_total','text',redirected_page,domain,webpage)
	return webpage
	
def reinit_pool():
#	try:
#		pool.close()
#	except:
#		pass
	pool_size = int(multiprocessing.cpu_count())
	pool_size= 10*pool_size
	pool = multiprocessing.Pool(processes=pool_size)
	return pool,pool_size


	
class crawler:
	
  # Initialize the crawler with the name of database
	def __init__(self,dbname):
		self.con=sqlite3.connect(dbname)
  
	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()

  # Auxilliary function for getting an entry id and adding 
  # it if it's not present
	def getentryid(self,table,field,value,createnew=True):
		#print 'field',field,value
		cur=self.con.execute("select rowid from %s where %s='%s'" % (table,field,value))
		res=cur.fetchone()
		if res==None:
			cur=self.con.execute("insert into %s (%s) values ('%s')" % (table,field,value))
			return cur.lastrowid
		else:
	  		return res[0]

	def addtocorpus(self,webpage,table='urlcorpus'):
		#print 'adding to corpus '+url
		urlid=self.getentryid('urllist','url',webpage.url)
		if 1:
	  		try:
				#self.con.execute("insert into urlcorpus(urlid,url,text_summary,html_summary,html,md5,title,domain,url_feed,links,charset) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (urlid,unicode(webpage.url),unicode(webpage.text_summary).replace("'","''"),unicode(webpage.html_summary).replace("'","''"),unicode(webpage.html).replace("'","''"),webpage.md5,unicode(webpage.title).replace("'","''"),webpage.domain,webpage.url_feed,'*#*'.join(webpage.links),webpage.charset))
				self.con.execute("insert into urlcorpus(urlid,url,text_summary,html_summary,html,md5,title,domain,url_feed,links,charset,date) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (urlid,unicode(webpage.url),unicode(webpage.text_summary).replace("'","''"),unicode(webpage.html_summary).replace("'","''"),unicode(webpage.html).replace("'","''"),webpage.md5,unicode(webpage.title).replace("'","''"),webpage.domain,webpage.url_feed,'*#*'.join(webpage.links),webpage.charset,webpage.date))
				#self.con.execute("insert into urlcorpus(urlid,html_summary) values ('%s','%s')" % (urlid,unicode(webpage.html_summary).replace("'","''")))
			except:
				print 'fail to execute',webpage.url
				#webpage.display_page()
				#print "insert into urlcorpus(urlid,url,text) values ('%s','%s','%s')" % (urlid,unicode(url),unicode(html_txt))

  # Index an individual page
	def addtoindex(self,url,table='urllist'):
		if self.isindexed(url): return
		urlid=self.getentryid('urllist','url',url)	  

  # Return true if this url is already indexed
	def isindexed(self,url):
		return False
  
  # Add a link between two pages
	def addlinkref(self,urlFrom,urlTo,linkText):
		fromid=self.getentryid('urllist','url',urlFrom)
		toid=self.getentryid('urllist','url',urlTo)
		if fromid==toid: return
		cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
		linkid=cur.lastrowid


	def addlinkref_whole(self,urlFrom,urlTo,linkText):
		fromid=self.getentryid('urllist','url',urlFrom)
		toid=self.getentryid('urllist','url',urlTo)
		if fromid==toid: return
		cur=self.con.execute("insert into link_whole(fromid,toid) values (%d,%d)" % (fromid,toid))
		linkid=cur.lastrowid


	def crawl(self,pages,query='',inlinks=1,depth=10):	
		
		equivalent={}
		
		#print 'pages',pages 
		pagenumber=0
		for i in range(depth):
			
			pages_clean = {}
			for page,views in pages.iteritems():
				pages_clean[equivalent.get(page,page)]=views
			pages=pages_clean
			
			above_in_links_limit_pages=[x for x in pages if pages[x]>=inlinks and pages[x]<=50000]#on essaye de rouvrir la page 5 fois avant d'abandonner 
			N=len(above_in_links_limit_pages)			
			print '\n\n\n*****************************\n\n\n',i+1,'th thread - ',len(above_in_links_limit_pages),' pages to (re)check', ' over potentially ', len(pages.keys()) , ' total pages\n\n\n*****************************\n\n\n',
			print 'above_in_links_limit_pages',N
			
			
			#pool_size = int(multiprocessing.cpu_count())
			#pool_size = max(1,min(30*pool_size,len(above_in_links_limit_pages)))
			#pool_size=1#DEBUG MODE
			#print 'package',package
			try:
				pool.close()
			except:
				pass	
			pool,pool_size=reinit_pool()
			paquets=pool_size*50
			for j in range(N/paquets + 1):

				print "\n1#################processing packet, ",j,"over ",N/paquets, "eack stack has", paquets, " items\n"
				package =[]
				for page in above_in_links_limit_pages[j*paquets:(j+1)*paquets]:
					package.append((page,query))
			
			
				pool.close()
				pool,pool_size=reinit_pool()
				data_extracted = ''
			
				data_extracted=pool.map(extract_data, package,chunksize=10)
				if len(data_extracted)>0: 
					for webpage in data_extracted:
						if webpage.successful_open:
							pages[webpage.url]=-9999999999#page visited even if there is a redirection...
							if not webpage.url_redirected==None:
								equivalent[webpage.url]=webpage.url_redirected
				
					print 'data_extracted length',len(data_extracted)
					pool.close()
					pool,pool_size=reinit_pool()
					processed_pages=''
					processed_pages = pool.map(extract_links,data_extracted,chunksize=10) #extract_links returns: (page,soup,html,link_total)
					print 'total processed_pages = ',len(processed_pages)
					for processed_page in processed_pages:
						current_webpage=processed_page
						if current_webpage.successful_open:
							pages[current_webpage.url]=-9999999999#page visited
						else:
							pages[current_webpage.url]=pages[current_webpage.url]+100000#page visited
						if not current_webpage.links=='link_total':
							pagenumber+=1
							#if pagenumber%20==0:
							print pagenumber, 'th page recorded: ', current_webpage.url
							self.addtoindex(current_webpage.url)
							self.addtocorpus(current_webpage)
							for link in current_webpage.links:
								self.addlinkref(current_webpage.url,equivalent.get(link,link),'')				
								pages[link]=pages.get(link,0)+1				 				
							for link in current_webpage.links_whole:
								self.addlinkref_whole(current_webpage.url,equivalent.get(link,link),'')				
								#pages[link]=pages.get(link,0)+1
					self.dbcommit()
  
  # Create the database tables
	def createindextables(self): 
		self.con.execute('create table urllist(url text,url_redirect text ,url_views integer)')
		self.con.execute('create table urlcorpus(urlid Integer,url text,text_summary text,html_summary text, html text,md5 text,title text,domain text,url_feed text,links text,charset text,date text )')
		self.con.execute('create table link(fromid integer,toid integer)')
		self.con.execute('create table link_whole(fromid integer,toid integer)')
		self.con.execute('create index urlidx on urllist(url)')
		self.con.execute('create index urltoidx on link(toid)')
		self.con.execute('create index urlfromidx on link(fromid)')
		self.dbcommit()



