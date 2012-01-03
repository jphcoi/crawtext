#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import sqlite3
query='algues vertes AND sangliers'
#query='biofuel'

crawler=con=sqlite3.connect('ouput/'+query+'_crawl.db')

cur=con.execute("select urlid,domain from urlcorpus ")
res=cur.fetchall()
print res
pages = {}
for result in res:
	#pages[result[0]]=result[1].replace(',','_')[10:70]
	#pages[result[0]]='/'.join(result[1].replace('http://','').split('/')[:1]).replace("www.",'')
	pages[result[0]]=result[1]
print pages
def unique(list):
	list_clean = []
	for item in list:
		if not item in list_clean:
			list_clean.append(item)
	return list_clean

print (len(pages)), ' web pages '
print (len(unique(pages.values()))), ' unique sites '
cur=con.execute("select fromid,toid from link ")
links=cur.fetchall()
output = open('ouput/net.csv','w')
num_links=0

#for page in pages:
#	output.write(pages[page]+'\t'+pages[page]+'\n')
link_list=[]
for link in links:
	(fromid,toid)=link
	if fromid in pages and toid in pages:
		chaine=pages[fromid]+'\t'+pages[toid]
		if not chaine in link_list:
			link_list.append(chaine)
		if  1:# not 'alvinet' in chaine and not 'cle.wn.com' in chaine:
			output.write(chaine+'\n')
			num_links+=1
print num_links,'total links'
print len(link_list),'total unique links'




cur=con.execute("select fromid,toid from link_whole ")
links=cur.fetchall()
output = open('ouput/net_whole.csv','w')
num_links=0

#for page in pages:
#	output.write(pages[page]+'\t'+pages[page]+'\n')
link_list=[]
for link in links:
	(fromid,toid)=link
	if fromid in pages and toid in pages :
		chaine=pages[fromid]+'\t'+pages[toid]
		if not pages[fromid]==pages[toid]:
			if not chaine in link_list:
				link_list.append(chaine)
			if  1:# not 'alvinet' in chaine and not 'cle.wn.com' in chaine:
				output.write(chaine+'\n')
				num_links+=1
print num_links,'total links'
print len(link_list),'total unique links'