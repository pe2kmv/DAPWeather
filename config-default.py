#enter the credentials of your DAPNet account
#datenotation determines way of date display. Options: 'en' = ([month]/[day]/[year]; 'de' = [day].[month].[year]; 'nl' = [day]-[month]-[year]
#set 'debug' to True or False to trigger log output to dapweather.log
user = dict(
	username = 'Your DAPNet username',
	password = 'Your DAPNET password',
	datenotation = 'en',
	debug = False
)
#The section below contains the target details of the message
#callsign --> the call sign as listed at DAPNet
#transmittergrp --> the transmitter group the message needs to be sent to
#corerul --> the url of the REST API
pager = dict(
	callsign = 'target call sign',
	transmittergrp = 'target transmitter group',
	coreurl = 'http://www.hampager.de:8080/calls'
)
#Create a free account at www.openweathermap.org. Afterwards you'll be able to create your API key
#url --> this contains the API url at openweathermap.org
#key --> enter the API key you've generated via your openweathermap account
#ahead --> number of hours forecasted ahead; integer value 3-120 (range between 3 hours and 5 day forecast)
weather = dict(
	url = 'http://api.openweathermap.org/data/2.5/forecast',
	key='Your API key of openweathermap.org',
	city='A city of your choice',
	countrycode = 'The corresponding country code matching the selected city ',
	units = 'metric',
	ahead = 12
)
