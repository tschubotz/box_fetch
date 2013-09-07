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
Sms Notification Parameters class holds basic sms information
"""

class SendSmsNotificationsParameters(object):
	
	def __init__(self):
		self.params = {}
		self.callbackReference = {}
		
	def setCallbackData(self, callbackData):
		self.callbackReference['callbackData'] = callbackData
		
	def setNotifyURL(self, notifyURL):
		self.callbackReference['notifyURL'] = notifyURL
		
	def setFilterCriteria(self, criteria):
		self.params['filterCriteria'] = criteria
		
	def setClientCorrelator(self, clientCorrelator):
		self.params['clientCorrelator'] = clientCorrelator
		
	def parameters(self):
		self.params['callbackReference'] = self.callbackReference
		ret = {}
		ret['deliveryReceiptSubscription'] = self.params
		
		return ret
	
	