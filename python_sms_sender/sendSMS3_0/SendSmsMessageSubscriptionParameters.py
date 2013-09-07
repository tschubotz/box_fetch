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
Sms Message Subscription Parameters class holds basic sms receive subscription information
"""
class SendSmsMessageSubscriptionParameters(object):
	
	def __init__(self):
		self.params = {}
		self.callbackreference = {}
		
	def callbackData(self, callbackData):
		self.callbackreference['callbackData'] = callbackData
		
	def notifyURL(self, notifyURL):
		self.callbackreference['notifyURL'] = notifyURL
		
	def criteria(self, criteria):
		self.params['criteria'] = criteria
		
	def destinationAddress(self, destinationAddress):
		self.params['destinationAddress'] = destinationAddress
		
	def notificationFormat(self, notificationFormat):
		self.params['notificationFormat'] = notificationFormat
		
	def clientCorrelator(self, clientCorrelator):
		self.params['clientCorrelator'] = clientCorrelator
		
	def account(self, account):
		self.params['account'] = account
		
	def parameters(self):
		ret = {}
		self.params['callbackReference'] = self.callbackreference
		ret['subscription'] = self.params
		
		return ret