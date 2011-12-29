#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
reload(sys) 
sys.setdefaultencoding("utf-8")
import urllib2
from BeautifulSoup import *
import BeautifulSoup
from urlparse import urljoin
from sqlite3 import *
import sqlite3
#import nn
from pyparsing import *
import urllib
#import html2text
from random import choice
from library import *
#import html2text2
import multiprocessing
#mynet=nn.searchnet('nn.db')
import socket
from lxml import html
from lxml.html.clean import clean_html
sys.path.append("decruft")
#from decruft import Document
import decruft
import urllib2
import feedparser
from  pattern import web
from  pattern.web import *

from BeautifulSoup import BeautifulSoup as parser
from urlparse import urljoin
#from pattern.web import *
import warnings
import chardet
import time
warnings.filterwarnings("ignore")


socket.setdefaulttimeout(30)


headers = { 'User-Agent' : 'Mozilla/5.0' }
headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2' }
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2
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
	if check_query(query,str(html)):
		try:
			html_summary=decruft.Document(html).summary()
			text_summary=web.plaintext(html_summary, keep=[], replace=web.blocks, linebreaks=2, indentation=False)
		except:
			print 'cant use generic tools to get a summary'
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
	# def display_page(self):
	# 	print 'page url: ','url'

def extract_data(package):
	(page,query)=(package[0],package[1])
	#print page
	new_webpage=Webpage()
	new_webpage.url=page
	try:
		url=URL(page,method=GET)
		domain = url.domain# u'domain.com'
		url_feed=''
		redirected_page=url.redirect# Actual URL after redirection, or None.		
		path= url.path# [u'path']

		# different options to open a webpage
		html=url.download(user_agent=choice(user_agents),cached=False)
		#html = urllib2.urlopen(page).read()
	except:
		try:
			print "*** Could not open page: %s" % page
		except:
			try:
				html = urllib2.urlopen(page).read()
				print "****** Saved by urllib2 library which opened page: %s" % page
			except:
				pass
	try:
		dom = web.Document(html)
		try:
			title = dom.by_tag('title')[0]		
			title = repr(plaintext(title.content))
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

		print 'page: ', page,' with title: ', title,' was assessed as ',query_result
		if not redirected_page==None:
			print 'plus redirection: ',redirected_page
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
		new_webpage.successful_open=True
		#new_webpage.display_page()
		#new_webpage.links=None
	except:
		print "*** Could not extract data from %s" % page
	return new_webpage

def gettextonly_out(soup):
	v=soup.string
	#print 'v',v
	if v==Null:	  
	  c=soup.contents

	  resulttext=''
	  for t in c:
		subtext=gettextonly_out(t)
		try:
		  resulttext+=subtext.replace("'"," ")+'\n'
		except:
		  resulttext+=subtext+'\n'
	  return resulttext
	else:
	  return v.replace("'"," ").strip()

def find_url(domain,page,text,only_out=True):
	soup=parser(text)
	links=soup('a')
	#print 'links',links
	links_final=[]
	print 'domain',domain
	page_root = page.replace('http://','').replace('www','').split('/')[0]
	for link in links:	
		try:
			if ('href' in dict(link.attrs)):
				url=urljoin(page,link['href'])
				if url.find("'")!=-1: continue
				url=url.split('#')[0]	 # remove location portion
				if url[0:4]=='http':
					if domain=='google.com':
						url=url.split("&amp;")[0]
					if only_out:
						link_root=link['href'].replace('http://','').replace('www','').split('/')[0]
						if link_root!=page_root:
							links_final.append(url)
					else:
						links_final.append(url)
		except:
			pass
	return links_final

	
def extract_links(webpage):
	#(page,html,querycheck,rssfeed_url,text,redirected_page,html_summary,domain,webpage)=data
	link_total=[]
	page_old=webpage.url
	if not webpage.url_redirected==None: 
		webpage.url=webpage.url_redirected
	if webpage.query_result:
		#links=unique(web.find_urls(html_summary, unique=True))
		links=unique(find_url(webpage.domain,webpage.url,webpage.html_summary,only_out=False))#on chercher les liens uniquement dans le contenu pertinent
		for link in links:#in find_url(page,html):#web.find_urls(text, unique=True):
			if not check_forbidden(link):
					linkText=''
					if not link[0:4]=='http':
						link = 'http//'+link
					else:
						link_total.append((webpage.url,link,linkText))
		print 'investigating a new page ', webpage.url, ' with ', len(link_total), ' citation links'
		soup=''
		webpage.links = link_total
		#return (page_old,soup,html,link_total,text,redirected_page,domain,webpage)
	else:
		webpage.links='link_total'
		#return (page_old,'soup','html','link_total','text',redirected_page,domain,webpage)
	return webpage
	

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

	def addtocorpus(self,url,html,html_txt,table='urlcorpus'):
		#print 'adding to corpus '+url
		urlid=self.getentryid('urllist','url',url)
		if 1:
	  		try:
				self.con.execute("insert into urlcorpus(urlid,url,text) values ('%s','%s','%s')" % (urlid,unicode(url),unicode(html_txt).replace("'"," ")))
			except:
				print 'fail to execute',url
				print "insert into urlcorpus(urlid,url,text) values ('%s','%s','%s')" % (urlid,unicode(url),unicode(html_txt))

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


	def crawl(self,pages,query='',inlinks=1,depth=10):	
		pool_size = int(multiprocessing.cpu_count())
		pool_size= 10*pool_size
		pool = multiprocessing.Pool(processes=pool_size)
		#print 'pages',pages 
		pagenumber=0
		for i in range(depth):
			above_in_links_limit_pages=[x for x in pages if pages[x]>=inlinks]
			print i+1,'th thread - ',len(above_in_links_limit_pages),' pages to (re)check', ' over potentially ', len(pages.keys()) , ' total pages '
			print 'above_in_links_limit_pages',len(above_in_links_limit_pages)
			#pool_size = int(multiprocessing.cpu_count())
			#pool_size = max(1,min(30*pool_size,len(above_in_links_limit_pages)))
			#pool_size=1#DEBUG MODE
			package =[]
			for page in above_in_links_limit_pages:
				package.append((page,query))
			print 'package',package
			#data_extracted = []
			#r = pool.map_async(extract_data, package,callback=data_extracted.append)#check the current page against the query
			data_extracted=pool.map(extract_data, package)
			print "thread",i+1," wait... "
			#r.wait()

			if len(data_extracted)>0:
				#data_extracted=data_extracted[0]
				print 'data_extracted length',len(data_extracted)
				processed_pages = pool.map(extract_links,data_extracted) #extract_links returns: (page,soup,html,link_total)
				print 'total processed_pages = ',len(processed_pages)
				for processed_page in processed_pages:
					current_webpage=processed_page
					redirected_page=current_webpage.url_redirected
					if not redirected_page==None and not redirected_page=='redirected_page':#in case of redirection
						try:
							del(pages[current_webpage.url])	
						except:
							print current_webpage.url, ' was not in global dictionnary pages...?'
							pass
						current_webpage.url=current_webpage.url_redirected
					if not check_forbidden(current_webpage.url):
						#print 'should change status of page ', page	, ' to -999999...
						pages[current_webpage.url]=-9999999999#page visited
						if not current_webpage.links=='link_total':
							pagenumber+=1
							if pagenumber%20:
								print pagenumber, 'th page recorded: ', page
							self.addtoindex(current_webpage.url)
							self.addtocorpus(current_webpage.url,current_webpage.html_summary,current_webpage.text_summary)
							for (page,cited,linkText) in current_webpage.links:
								self.addlinkref(current_webpage.url,cited,linkText)				
								pages[cited]=pages.get(cited,0)+1				 				
							self.dbcommit()
			else:
				print 'no more websites to visit'
				break
  
  # Create the database tables
	def createindextables(self): 
		self.con.execute('create table urllist(url text,url_redirect text ,url_views integer)')
		self.con.execute('create table urlcorpus(urlid Integer,url text,text text)')
		self.con.execute('create table link(fromid integer,toid integer)')
		self.con.execute('create index urlidx on urllist(url)')
		self.con.execute('create index urltoidx on link(toid)')
		self.con.execute('create index urlfromidx on link(fromid)')
		self.dbcommit()

