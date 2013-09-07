"""
This file is part of the Telekom Python SDK
Copyright 2013 Deutsche Telekom AG

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

"""
Sms Parameters class holds basic sms information e.g message, senderAddress etc.
"""

class SendSmsParameters(object):
	
	def __init__(self):
		self.address = []
		self.params = {}
		self.outboundDic = {}
		self.receiptRequest = {}
		self.flash = False
		self.binary = False
		
	def addAddress(self, address):
		self.address.append("tel:" + address)
		
	def setClientCorrelator(self, clientCorrelator):
		self.params['clientCorrelator'] = clientCorrelator
		
	def setMessage(self, message):
		self.outboundDic['message'] = message
		
	def setFlashMessage(self, flashMessage):
		self.outboundDic['flashMessage'] = flashMessage
		self.flash = True
		
	def setBinaryMessag(self, binaryMessage):
		self.outboundDic['message'] = binaryMessage
		self.binary = True
		
	def setNotifyURL(self, notifyURL):
		self.receiptRequest['notifyURL'] = notifyURL
		
	def setCallbackData(self, callbackData):
		self.receiptRequest['callbackData'] = callbackData
		
	def setSendername(self, sendername):
		self.params['senderName'] = sendername
		
	def setSenderAddress(self, senderaddress):
		self.params['senderAddress'] = senderaddress
		
	def setAccount(self, account):
		self.params['account'] = account
		
	def setOutboundEncoding(self, encoding):
		self.params['outboundEncoding'] = encoding
		
	def parameters(self):
		ret = {}

		self.params["address"] = self.address
		
		if self.flash:
			self.params['outboundSMSFlashMessage'] = self.outboundDic
		elif self.binary:
			self.params['outboundSMSBinaryMessage'] = self.outboundDic
		else:
			self.params['outboundSMSTextMessage'] = self.outboundDic
		
		if(self.receiptRequest != {}):
			self.params['receiptRequest'] = self.receiptRequest
		
		ret['outboundSMSMessageRequest'] = self.params
		
		return ret;
			
		