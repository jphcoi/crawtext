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

def check_forbidden(url):
	for forbid in forbidden_sites:
		if forbid in url:
			print url, ' declined (fordbideen list)'
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
	return url