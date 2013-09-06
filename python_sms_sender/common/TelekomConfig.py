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

"""
Configuration class, holds basic information 
needed for further interaction with the backend server.
"""
class TelekomConfig(object):
	
	def __init__(self, config, proxy=None):
		
		self.config = config
		
		# Basic configuration params
		self.SDK_VERSION = "Telekom Python SDK/4.0"
		self.SDK_AUTH = "TAuth realm=\"https://odg.t-online.de\""
		self.SDK_ACCEPT = "application/json"
		self.SDK_CONTENT_TYPE = "application/json"
		
		if proxy != None:
			self.proxy = proxy
		
		if config:
			self.username = config["username"]
			self.password = config["password"]
			self.apiBaseUrl = config["apiBaseUrl"]
			self.environment = config["environment"]
			self.apiAuthUrl = config["apiAuthUrl"]