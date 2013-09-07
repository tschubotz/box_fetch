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

import TelekomJSONService
import time

"""
Basic Authentication class for the Telekom SDK
"""
class TelekomAuth(object):
	
	def __init__(self, service):
		self.service = service
		
	def isValidToken(self):
		"Method checks, whether token is valid."
		return self.secureTokenValidUntil >= time.time()
	
	def setSecureToken(self, token):
		"Method sets the secure STS token"
		self.secureToken = token
		
	def setSecureTokenValidUntil(self, validUntil):
		"Method sets the validation date"
		self.secureTokenValidUntil = validUntil
	
	def setService(self, service):
		"Method sets the service class provided for authentication"
		self.service = service