# DAPWeather

DAPWeather has been written to be able to pull weather forecast data from OpenWeatherMap.org and convert it into a pager message.

This script is based on Python 3.x --> review DEPENDENCIES to have all additional libraries installed

Prerequisites to be able to use the script are:
- valid account for DAPNet (http://www.hampager.de)
- valid account for OpenWeatherMap.org (www.openweathermap.org)

Before running the script, change the settings in the file config.cfg:

Section 'user' contains the user specific details:
	- username = DAPNet user name
	- password = DAPNet password
	- datenotation = determines date format in the pager message. Available options:
		'nl' = dutch date format --> [day]-[month]-[year]
		'de' = german date format --> [day].[month].[year]
		'en' = international date format --> [month]/[day]/[year]
		
Section 'dapnet' contains details related to the DAPNet target call sign, transmitter group and API URL
	- callsign = target call sign for the messages as setup via www.hampager.de
	- transmittergrp = transmitter group as setup via www.hampager.de to determine range of the message
	- baseurl = URL and port of the DAPNET API
	- coreurl = path added to baseurl to be able to send calls
	- trxurl = path added to baseurl to query transmitter status

Section 'aprsis' has been added to be able to share config files with DAPNETAPRS.
	- username = aprs-is username / call sign
	- password = aprs passcode
	- sourcecall = callsign acting as owner of sent objects
	- apikey = aprs-is API key, already included for possible future needs
	
Section 'weather' contains all details regarding the OpenWeatherMap.org account and the parameters to query data from this service:
	- url = OpenWeatherMap API URL for 5 days forecast in 3 hour intervals
	- key = API key from OpenWeatherMap (can be generated via account details)
	- city = city of the weather forecast. Visit OpenWeatherMap.org for all available options
	- countrycode = country code of the city selected above
	- units = selection between metric or imperial system. Available options:
		- metric = metric system (degrees Celsius, (milli-)meters, hectopascal, etc)
		- imperial = imperial system (degrees Fahrenheit, feet, etc)
	- ahead = determines how many hours the forecast should look forward. Available options:
		- integer between 3 and 120
		- always use steps of 3

Section 'misc' contains some miscellanious parameters, not fitting in any other section.
	- logfile = full path and name of the log file to log errors / warnings
		
Usage:
- copy the files to a directory of your choice, preferably your home directory. Anyway the directory should not be accessible from outside / by any kind for server running as the configuration file contains user credentials!
- a user defined config file can be added as attribute in the script command line using '-c=[your config file name]. This enables you to have multiple config files prepared, to sent customized weather reports for specific regions.
- schedule a cron job to run the script in intervals of your choice. Choose wisely and avoid heavy traffic via DAPNet.
		
Ronald Bouwens - PE2KMV - May 4th. 2017
