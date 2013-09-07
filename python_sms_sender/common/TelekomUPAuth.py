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
from TelekomAuth import TelekomAuth

"""
Default authentication class for username/password authentication.
"""
class TelekomUPAuth(TelekomAuth):
	
	def performAuth(self):
		tokenData = self.service.getResponseTokenData(self.service.config.apiAuthUrl)
		self.setTokenData(tokenData)
		return self.secureToken
	
	def setTokenData(self, tokenData):
		self.setSecureToken(tokenData["token"])
		self.setSecureTokenValidUntil(tokenData["expires"])
		