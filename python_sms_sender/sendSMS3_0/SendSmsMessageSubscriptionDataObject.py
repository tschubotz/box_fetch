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
Sms Message Subscription data object class holds basic sms receive subscription response data information
"""
class SendSmsMessageSubscriptionDataObject(object):
	
	def __init__(self, data):
		data = data['subscription']
		self.getCallbackReference(data['callbackReference'])
		
		if('criteria' in data.keys()):
			self.criteria = data['criteria']
			
		if('destinationAddress' in data.keys()):
			self.destinationAddress = data['destinationAddress']
			
		if('notificationFormat' in data.keys()):
			self.notificationFormat = data['notificationFormat']
			
		if('clientCorrelator' in data.keys()):
			self.clientCorrelator = data['clientCorrelator']
		
		if('account' in data.keys()):
			self.account = data['account']
		
		if('resourceURL' in data.keys()):
			self.resourceURL = data['resourceURL']
		
		
	def getCallbackReference(self, referenceData):
		if('callbackData' in referenceData.keys()):
			self.callbackData = referenceData['callbackData']
			
		if('notifyURL' in referenceData.keys()):
			self.notifyURL = referenceData['notifyURL']
		
	