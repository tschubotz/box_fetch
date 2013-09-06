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
Default data object for new Send SMS 3.0 responses
"""

from sendSMS3_0.SendSmsDeliveryStatusDataObject import SendSmsDeliveryStatusDataObject

class SendSmsDataObject(object):
	
	def __init__(self, data):
		if('outboundSMSMessageRequest' in data.keys()):
			self.getInfoData(data['outboundSMSMessageRequest'])
		elif('deliveryReceiptSubscription' in data.keys()):
			self.getDeliveryData(data['deliveryReceiptSubscription'])
		else:
			self.getInfoData(data)
		
	def getInfoData(self, data):
		
		if('deliveryInfoList' in data.keys()):
			self.deliveryInfo = data['deliveryInfoList']['deliveryInfo']
			
			self.deliveryInfos = []
			for d in self.deliveryInfo:
				self.deliveryInfos.append(SendSmsDeliveryStatusDataObject(d['address'], d['deliveryStatus']))
			
			if('resourceURL' in data['deliveryInfoList'].keys()):
				self.resourceURL = data['deliveryInfoList']['resourceURL']
			else:
				self.resourceURL = ""
			
		if('receiptRequest' in data.keys()):
			self.notifyURL = data['receiptRequest']['notifyURL']
			self.callbackData = data['receiptRequest']['callbackData']
			
	def getDeliveryData(self, data):
		if('callbackReference' in data.keys()):
			self.callbackData = data['callbackReference']['callbackData']
			self.notifyURL = data['callbackReference']['notifyURL']
		if('filterCriteria' in data.keys()):
			self.filterCriteria = data['filterCriteria']
		if('resourceURL' in data.keys()):
			self.resourceURL = data['resourceURL']
			
	def deliveryInfo(self):
		return self.deliveryInfo
	
	def resourceUrl(self):
		return self.resourceURL
	
	def notifyURL(self):
		return self.notifyURL
	
	def callbackData(self):
		return self.callbackData
	
	def filterCriteria(self):
		return self.filterCriteria
	
	
	
	