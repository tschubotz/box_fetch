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

from sendSMS3_0.SendSmsMessageDataObject import SendSmsMessageDataObject

class SendSmsReceiveDataObject(object):
	
	def __init__(self, data):
		self.prepareMessages(data['inboundSMSMessageList'])
		self.numberOfMessagesInThisBatch = data['inboundSMSMessageList']['numberOfMessagesInThisBatch']
		self.resourceURL = data['inboundSMSMessageList']['resourceURL']
		self.totalNumberOfPendingMessages = data['inboundSMSMessageList']['totalNumberOfPendingMessages']
	
	def prepareMessages(self, data):
		self.messages = []
		messages = data['inboundSMSMessage']
		
		for m in messages:
			obj = SendSmsMessageDataObject(m['dateTime'], m['destinationAddress'], m['messageId'], m['resourceURL'], m['senderAddress'], m['message'])
			self.messages.append(obj)
	
	def getMessages(self):
		return self.messages
	
	