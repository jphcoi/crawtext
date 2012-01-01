#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Jean-Philippe Cointet on 2011-12-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

forbidden_sites=map(lambda x: x[:-1],open('forbidden_sites.txt','r').readlines())
print 'forbidden_sites',forbidden_sites
forbidden_linktext=map(lambda x: x[:-1],open('forbidden_linktext.txt','r').readlines())
print 'forbidden_linktext',forbidden_linktext

def check_forbidden(urle):
	(url,urltxt)=urle
	for forbid in forbidden_sites:
		if forbid in url:
			print url, ' declined (fordbideen list)'
			return True
	for forbidtxt in forbidden_linktext:
		if forbidtxt==urltxt.lower():
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
