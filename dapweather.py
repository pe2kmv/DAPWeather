#DAPWeather can be used to send messages with weather data via DAPNet
#All variables / credentials are to be set in the file config.py
#Ronald Bouwens - PE2KMV, april 2017

#this script is layed out for Python 3
#make sure to install the correct Python 3 packages to have all functions available


#import the configuration file
import config
import requests
import urllib.request
import json
import decimal
import os.path
import datetime
import time


#assign variables with data of the config file
username = config.user['username']
password = config.user['password']
datenotation = config.user['datenotation']
callsign = config.pager['callsign']
transmittergrp = config.pager['transmittergrp']
coreurl = config.pager['coreurl']
weatherurl = config.weather['url']
weathercity = config.weather['city']
weathercountry = config.weather['countrycode']
weatherapi = config.weather['key']
weatherunits = config.weather['units']
weatherahead = int(config.weather['ahead']/3)
debugmode = config.user['debug']
logfile = 'dapweather.log'

#date and time converter
def convert_date(unixtime):
	if datenotation is 'nl':
		outputdate = datetime.datetime.fromtimestamp(unixtime).strftime('%d-%m-%Y %H:%M')
	elif datenotation is 'de':
		outputdate = datetime.datetime.fromtimestamp(unixtime).strftime('%d.%m.%Y %H:%M')
	else:
		outputdate = datetime.datetime.fromtimestamp(unixtime).strftime('%m/%d/%Y %H:%M')
	return outputdate

#get weather data
#complete the url with location and api
def create_url(cityname,countryname):
	full_url = weatherurl + '?q=' + cityname + "," + countryname + '&mode=json&units=' + weatherunits + '&APPID=' + weatherapi
	return full_url

#fetch data
def data_fetch(full_url):
	url = urllib.request.urlopen(full_url)
	output = url.read().decode('utf-8')
	raw_api_dict = json.loads(output)
	url.close()
	return raw_api_dict

def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('city').get('name'),
        temp=round(raw_api_dict.get('list')[weatherahead].get('main').get('temp'),1),
        pressure=int(raw_api_dict.get('list')[weatherahead].get('main').get('pressure')),
        wind=int(raw_api_dict.get('list')[weatherahead].get('wind').get('speed')),
        wind_deg=int(raw_api_dict.get('list')[weatherahead].get('wind').get('deg')),
        dtx=convert_date(raw_api_dict.get('list')[weatherahead].get('dt')),
        clouds=raw_api_dict.get('list')[weatherahead].get('weather')[0].get('description'),
    )
    return data

def data_output(data):
	weather = data['city'] + ' ' + data['dtx'] + ': T: ' + str(data['temp']) + 'C, P: '+ str(data['pressure']) + 'HPa, wind: ' + str(data['wind']) + 'm/s ' + str(data['wind_deg']) + 'deg '
	return weather

#send page
msgtext = data_output(data_organizer(data_fetch(create_url(weathercity,weathercountry))))
requests.post(coreurl,auth=(username,password),json={'text':msgtext,'callSignNames':[callsign],'transmitterGroupNames':[transmittergrp],'emergency':False})

#if debug mode is enabled, check whether log file exists, if necessary create and write log
if debugmode:
	now = datetime.datetime.now()
	timestamp = str(now.year) + str(now.month) + str(now.day) + ' ' + str(now.hour) + str(now.minute) + str(now.second)
	if os.path.isfile(logfile):
		debugfile = open(logfile,'a')
	else:
		debugfile = open(logfile,'w')
	debugfile.write(timestamp + ': Details: callsign ' + callsign + ' | trxgroup ' + transmittergrp + '\n')
	debugfile.write(timestamp + ': ' + msgtext +'\n')
	debugfile.write('\n')
