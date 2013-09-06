"""
This file is part of the Telekom Python SDK
Copyright 2012 Deutsche Telekom AG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
import urllib2
import urllib
import MultipartPostHandler
import json
import time

import httplib
import sys
from TelekomDataObject import TelekomDataObject
from TelekomException import TelekomException
from TelekomRequestException import TelekomRequestException

"""
Standard class for interactions with the server.
Holds methods for standard REST calls and multipart/form-data communication.
"""
class TelekomJSONService(object):

	def __init__(self, config={}):
		self.config = config
		
	def getResponseTokenData(self, url=None, addtionalOptions=None):
		"Method request a new token for further communications."
		
		if url != None:
			self.apiAuthUrl = url
		
		# encode basic header for credentials
		basicheader = base64.b64encode(self.config.username+':'+self.config.password)
		
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(realm="TAuth", uri="https://odg.t-online.de", user=self.config.username, passwd=self.config.password)
		
		# check whether proxy is present
		if "proxy" in globals():
			proxy_handler = urllib2.ProxyHandler(self.config.proxy)
			opener = urllib2.build_opener(proxy_handler, auth_handler)
		else:
			opener = urllib2.build_opener(auth_handler)
		
		# set request headers
		urllib2.install_opener(opener)
		req = urllib2.Request(self.apiAuthUrl)
		req.add_header('Accept', 'application/json')
		req.add_header('Authorization', 'Basic '+basicheader)
		
		# send request
		try:
			response = urllib2.urlopen(req)
			i = response.info() # http header information
			
			t = time.strptime(i['expires'], "%a, %d %b %Y %H:%M:%S GMT") # expire date in seconds converted
		
			dic = json.loads(response.read()) # append list with expiration date
			dic["expires"] = time.mktime(t)
	
			return dic
	
		except urllib2.HTTPError as e: # catch wrong username or password
		
			raise RuntimeError('username or password invalid!')

	def getResponseStandardData(self, url, secureToken, request="GET", dic=None, additionalOptions=None):
		"Method sends a standard REST call. Default is 'GET'."
				
		if dic != None: # check whether parameters are given
			dic = dic.parameters()
		
		if "proxy" in globals(): # set proxy if necessary
			proxy_handler = urllib2.ProxyHandler(self.config.proxy)
			opener = urllib2.build_opener(proxy_handler)
			urllib2.install_opener(opener)
		
		# check whether the body parameters have to be part of http-body or url
		data = ""
		if request == "GET":
			if dic:
				for e in dic:
					data += "&"+e+"="+urllib2.quote(dic[e]) # urlencode data
					
				data = data.split("&", 1)[1]
		else:
			if(dic != None):
				data = dic
				data = urllib.urlencode(data)
		
		if request == "POST":
			if data != "":
				req = urllib2.Request(url, data)
			else:
				req = urllib2.Request(url)
			req.get_method = lambda: 'POST'
		elif request == 'PUT' and dic != None:
			#url += '?' + '&'.join(e + "=" + urllib2.quote(dic[e]) for e in dic)
			req = urllib2.Request(url, data)
			req.get_method = lambda: 'PUT'
		elif request == 'GET' and dic != None:
			url += '?' + '&'.join(e + "=" + urllib2.quote(dic[e]) for e in dic)
			req = urllib2.Request(url)
		elif request == 'DELETE':
			req = urllib2.Request(url)
			req.get_method = lambda: 'DELETE'
		else:
			req = urllib2.Request(url)
		
		# define header fields	
		req.add_header('Authorization', self.config.SDK_AUTH+",oauth_token=\""+secureToken+"\"")
		req.add_header('User-Agent', self.config.SDK_VERSION)
		req.add_header('Accept', 'application/json')
		
		# establish call
		try:
			response = urllib2.urlopen(req)
			response = json.loads(response.read())
			return response
		
		except urllib2.HTTPError as e: # catch other status codes than '0000' and raise a new TelekomException containing 'statusCode' and 'statusMessage'
			raise TelekomException(json.loads(e.read()))
	
	def getResponseStandardDataForOAuth(self, url, secureToken, request="GET", dic=None, additionalOptions=None):
		"Method sends a standard REST call. Default is 'GET'."
		
		if dic != None: # check whether parameters are given
			dic = dic.parameters()
		
		if "proxy" in globals(): # set proxy if necessary
			proxy_handler = urllib2.ProxyHandler(self.config.proxy)
			opener = urllib2.build_opener(proxy_handler)
			
			### for debugging the request
			debughandler=urllib2.HTTPHandler(debuglevel=1)
			debugopener = urllib2.build_opener(debughandler)
			urllib2.install_opener(debugopener)
			###
			
			urllib2.install_opener(opener)
		
		# check whether the body parameters have to be part of http-body or url
		data = ""
		if request != "GET":
			data = json.dumps(dic, separators=(',',':'))
		
		if request == "POST":
			if data != "":
				req = urllib2.Request(url, data)
			else:
				req = urllib2.Request(url)
			req.get_method = lambda: 'POST'
		elif request == 'PUT' and dic != None:
			req = urllib2.Request(url, data)
			req.get_method = lambda: 'PUT'
		elif request == 'GET' and dic != None:
			url += '?' + '&'.join(e + "=" + urllib2.quote(dic[e]) for e in dic)
			req = urllib2.Request(url)
		elif request == 'DELETE':
			req = urllib2.Request(url)
			req.get_method = lambda: 'DELETE'
		else:
			req = urllib2.Request(url)
		
		# define header fields
		req.add_header('Authorization', self.config.SDK_AUTH+',oauth_token=\"'+secureToken+'\"')
		req.add_header('User-Agent', self.config.SDK_VERSION)
		req.add_header('Accept', 'application/json')
		req.add_header('Content-Type', 'application/json')
		
		# establish call
		try:
			response = urllib2.urlopen(req)
			resp = response.read()
			return resp
		
		except urllib2.HTTPError as e: # catch other status codes than '0000' and raise a new TelekomException containing 'statusCode' and 'statusMessage'
			error = e.read()
			print json.loads(error)
			raise TelekomRequestException(json.loads(error))
		
	def getResponseMixedData(self, url, secureToken, dic, additionalOptions=None):
		"Method sets up a REST call with mixed body data such as multipart/form-data."
		
		# check whether proxy is given
		if "proxy" in globals():
			proxy_handler = urllib2.ProxyHandler(self.config.proxy)
			opener = urllib2.build_opener(proxy_handler)
			urllib2.install_opener(opener)
				
		multipart = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
		urllib2.install_opener(multipart)
		
		req = urllib2.Request(url, dic.parameters())

		req.add_header('Authorization', self.config.SDK_AUTH+",oauth_token=\""+secureToken+"\"")
		req.add_header('User-Agent', self.config.SDK_VERSION)
		req.add_header('Accept', 'application/json')
		
		# sets additional header fields
		if additionalOptions != None:
			for key in additionalOptions:
				req.add_header(key, additionalOptions[key])
		
		try:
			response = urllib2.urlopen(req)
			
			response = json.loads(response.read())	
			
			return response
		
		except urllib2.HTTPError as e:
			
			raise TelekomException(json.loads(e.read()))
			
	def getResponseJSONData(self, url, secureToken, jsonString, additionalOptions=None):
		"Method sends a JSON encoded string via REST"
		
		if "proxy" in globals(): # set proxy if necessary
			proxy_handler = urllib2.ProxyHandler(self.config.proxy)
			opener = urllib2.build_opener(proxy_handler)
			urllib2.install_opener(opener)
		
		req = urllib2.Request(url, jsonString)
			
		# define header fields	
		req.add_header('Authorization', self.config.SDK_AUTH+",oauth_token=\""+secureToken+"\"")
		req.add_header('User-Agent', self.config.SDK_VERSION)
		req.add_header('Accept', 'application/json')
		req.add_header('Content-Type', 'application/json')
		#req.add_header('Content-Length', len(json))
		
		# establish call
		try:
			response = urllib2.urlopen(req)
			response = json.loads(response.read())
			
			return response
		
		except urllib2.HTTPError as e: # catch other status codes than '0000' and raise a new TelekomException containing 'statusCode' and 'statusMessage'
			
			raise TelekomException(json.loads(e.read()))
		
	def getResponseOAuthDataWithCredentials(self, url, requestDictionary):
		"Method retrieves access token via app credentials"
		
		request = 'POST';
		dic = requestDictionary;
		
		if "proxy" in globals(): # set proxy if necessary
			proxy_handler = urllib2.ProxyHandler(self.config.proxy)
			opener = urllib2.build_opener(proxy_handler)
			urllib2.install_opener(opener)
		
		client_id = requestDictionary['client_id'];
		client_secret = requestDictionary['client_secret'];
		del requestDictionary['client_id'];
		del requestDictionary['client_secret'];
			
		# encode basic header for credentials
		basicheader = base64.b64encode(client_id+':'+client_secret)
			
		# check whether the body parameters have to be part of http-body or url
		data = ""
		if dic:
			for e in dic:
				data += "&"+e+"="+urllib2.quote(dic[e]) # urlencode data
				
			data = data.split("&", 1)[1]
							
			req = urllib2.Request(url)
			req.get_method = lambda: 'POST'
				
		req.add_header('Authorization', 'Basic '+basicheader)
				
		# send request
		try:
			response = urllib2.urlopen(req, data)
			
			dic = json.loads(response.read()) # append list with expiration date
			
			return dic
			
		except urllib2.HTTPError as e: # catch wrong username or password
			raise TelekomException(json.loads(e.read()))
					