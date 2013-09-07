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
Default Exception handles request errors.
"""

class TelekomRequestException(Exception):
	
	def __init__(self, dic):
		if('requestError' in dic):
			dict = dic['requestError']
			if('policyException' in dict):
				self.getPolicyException(dict['policyException'])
			elif('serviceException' in dict):
				self.getPolicyException(dict['serviceException'])
		elif('status' in dic):
			self.getStandardError(dic['status'])
			
	def getPolicyException(self, dic):
		self.messageId = dic['messageId']
		self.text = dic['text']
		if('variables' in dic):
			self.variables = dic['variables']
	
	def getStandardError(self, dic):
		self.statusCode = dic['statusCode']
		self.statusMessage = dic['statusMessage']
	
	def __str__(self):
		return repr("Message ID: " + self.messageId + " ---- Text: " + self.text  + " ---- Variables: " + self.variables)