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

from common.TelekomJSONService import TelekomJSONService
from common.TelekomGCPConfig import TelekomGCPConfig
from common.TelekomOAuthGCP import TelekomOAuthGCP
from sendSMS3_0.SendSmsClient import SendSmsClient
from sendSMS3_0.SendSmsParameters import SendSmsParameters
from sendSMS3_0.SendSmsDataObject import SendSmsDataObject
from sendSMS3_0.SendSmsNotificationsParameters import SendSmsNotificationsParameters
from sendSMS3_0.SendSmsReceiveParameters import SendSmsReceiveParameters
from sendSMS3_0.SendSmsReceiveDataObject import SendSmsReceiveDataObject
from sendSMS3_0.SendSmsMessageSubscriptionDataObject import SendSmsMessageSubscriptionDataObject
from sendSMS3_0.SendSmsMessageSubscriptionParameters import SendSmsMessageSubscriptionParameters

import sys

"""
Simple sample for the Global SMS API.
Provides serveral how tos related to sendSMS functionality.
"""

if __name__ == '__main__':

	if len(sys.argv) < 3:
		print "usage: {0} <destination_number> <sms_text>".format(sys.argv[0])
		exit(1)

	destination_number = sys.argv[1]
	sms_text = " ".join(sys.argv[2:])

	# Prepare for GCP token
	url = "https://global.telekom.com/gcp-web-api/oauth"
	grant_type = "client_credentials"
	client_id = "dDwnYjrTwe"
	client_secret = "1637c4369119f82e3a51c8e0e7d7cbd5-e0b01a5e7aa80a3791fbc9f74670f33e-1c10e2bea0ce3176104680a6600de9a6"
	scope = "DC0QX4UK"
	params = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret,'scope':scope}
	configDict = {'url':url, 'params':params}

	# Basic settings
	apiBaseUrl = "https://gateway.developer.telekom.com"
	environment = "budget" # premium, budget, sandbox and mock
	conf = {"apiBaseUrl":apiBaseUrl, "environment":environment}

	# Initialize config
	#config = TelekomGCPConfig(conf) # proxy is optional

	# proxy = {'http':'<yourproxy>:<yourport>'} # must be protocol - url dict
	config = TelekomGCPConfig(conf) # proxy is optional

	# Initialize service
	service = TelekomJSONService(config)

	# Get OAuth token
	auth = TelekomOAuthGCP(service)
	token = auth.grantWithClientCredentials(configDict)
	# print token

	# Initialize client
	client = SendSmsClient(service)

	# Initialize parameters
	smsparameters = SendSmsParameters()
	smsparameters.addAddress(destination_number)
	# smsparameters.addAddress("+4915158584715")
	# smsparameters.setFlashMessage('TTTTK')
	smsparameters.setMessage(sms_text)
	smsparameters.setSenderAddress('0191011')

	#response = client.sendSMS(token, smsparameters, '<yourphonenumber>')
	response = client.sendSMS(token, smsparameters)