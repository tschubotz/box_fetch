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

import json
import urllib

from common.TelekomClient import TelekomClient
from sendSMS3_0.SendSmsDataObject import SendSmsDataObject
from sendSMS3_0.SendSmsReceiveDataObject import SendSmsReceiveDataObject
from sendSMS3_0.SendSmsMessageSubscriptionDataObject import SendSmsMessageSubscriptionDataObject

URL_KEY = "plone/sms/rest"
RESPONSE_KEY = "smsmessaging/v1"
"""
SMS Client supports feature to send a standard or flash sms to multiple numbers.
"""
class SendSmsClient(TelekomClient):
	
	"""
	Sends an SMS with specific parameters
	"""
	def sendSMS(self, secureToken, parameters, originator=None, additionalOptions=None):
		if additionalOptions != None:
			self.additionalOptions = additionalOptions
		
		if originator == None:
			originator = "0191011"
		else:	
			originator = urllib.quote_plus("tel:" + originator)
		
		url = self.buildResponseUrl(URL_KEY, RESPONSE_KEY) + "/outbound/" + originator + "/requests"
		
		print url
		
		response = self.service.getResponseStandardDataForOAuth(url, secureToken, "POST", parameters)
		
		return SendSmsDataObject(json.loads(response))
	
	"""
	Queries the delivery report of a previously sent SMS.
	Must specify the previously resource url
	"""
	def queryDeliveryReport(self, secureToken, resourceURL):
		if(resourceURL != None):
			response = self.service.getResponseStandardDataForOAuth(resourceURL, secureToken)
		return SendSmsDataObject(json.loads(response))
	
	"""
	Start subscription for delivery notifications
	"""
	def subscribeToDeliveryNotifications(self, secureToken, parameters, originator=None):
		
		if(originator == None):
			originator = '0191011'
		else:
			originator = urllib.quote_plus("tel:" + originator)
		
		url = self.buildResponseUrl(URL_KEY, RESPONSE_KEY) + "/outbound/" + originator + "/subscriptions"

		response = self.service.getResponseStandardDataForOAuth(url, secureToken, "POST", parameters)
		
		return SendSmsDataObject(json.loads(response))

	"""
	Stops a already excisting delivery notification subscription
	"""
	def stopSubscriptionToDeliveryNotifications(self, secureToken, resourceURL):
		if(resourceURL != None):
			
			urlid = resourceURL.split('/subscriptions/')[1]
			url = self.buildResponseUrl(URL_KEY, RESPONSE_KEY) + "/outbound/subscriptions/" + urlid

			self.service.getResponseStandardDataForOAuth(url, secureToken, "DELETE")
	
	"""
	Retrieve a SMS message from server
	"""
	def retrieveMessage(self, secureToken, parameters, registrationId):
		registrationId = 'tel:' + registrationId
		
		url = self.buildResponseUrl(URL_KEY, RESPONSE_KEY) + "/inbound/registrations/"+registrationId+"/messages"
		
		response = self.service.getResponseStandardDataForOAuth(url, secureToken, "GET", parameters)
		
		return SendSmsReceiveDataObject(json.loads(response))
	
	"""
	Start subscribing to notifications for SMS that have been sent to your Web application
	"""
	def subscribeToMessageNotifications(self, secureToken, parameters):
		
		url = self.buildResponseUrl(URL_KEY, RESPONSE_KEY) + "/inbound/subscriptions"
		
		response = self.service.getResponseStandardDataForOAuth(url, secureToken, "POST", parameters)

		return SendSmsMessageSubscriptionDataObject(json.loads(response))

	"""
	Stop subscribing to notifications for SMS that have been sent to your Web application
	"""
	def stopSubscriptionToMessageNotifications(self, secureToken, resourceURL):
		
		if(resourceURL != None):
			
			urlid = resourceURL.split('/subscriptions/')[1]
			url = self.buildResponseUrl(URL_KEY, RESPONSE_KEY) + "/inbound/subscriptions/" + urlid
			
			self.service.getResponseStandardDataForOAuth(url, secureToken, "DELETE")

		