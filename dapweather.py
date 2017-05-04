#DAPWeather can be used to send messages with weather data via DAPNet 
#All variables / credentials are to be set in the file config.py Ronald 
#Bouwens - PE2KMV, May 2017

#this script is layed out for Python 3
#make sure to install the correct Python 3 packages to have all functions available


#import the configuration file
import configparser
import requests
import urllib.request
import json
import decimal
import os.path
import datetime
import time
import argparse
import logging
import sys

logging.basicConfig(filename='dapnet.log',level=logging.CRITICAL)

#search for optional configuration file
parseObj = argparse.ArgumentParser()
parseObj.add_argument('-c','-config',type=str,help='Provide an optional config file',default='config.cfg')
args = parseObj.parse_args()

#assign configuration file to cfg
cfg = configparser.RawConfigParser()
cfg.read(args.c)

#setup logging system
logger = logging.getLogger('dapnet')
handler = logging.FileHandler(cfg.get('misc','logfile'))
logformat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(logformat)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

#assign variables with data of the config file
username = cfg.get('user','username')
password = cfg.get('user','password')
datenotation = cfg.get('user','datenotation')
callsign = cfg.get('dapnet','callsign')
transmittergrp = cfg.get('dapnet','transmittergrp')
baseurl = cfg.get('dapnet','baseurl')
coreurl = cfg.get('dapnet','coreurl')
weatherurl = cfg.get('weather','url')
weathercity = cfg.get('weather','city')
weathercountry = cfg.get('weather','countrycode')
weatherapi = cfg.get('weather','key')
weatherunits = cfg.get('weather','units')
weatherahead = int(int(cfg.get('weather','ahead'))/3)

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
	try:
		url = urllib.request.urlopen(full_url)
		output = url.read().decode('utf-8')
		raw_api_dict = json.loads(output)
		url.close()
	except:
		#no weather data retrieved, write log and bail out
		logger.error('Weather data could not be retrieved')
		sys.exit(0)
	else:	
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

req = requests.post(baseurl + coreurl,auth=(username,password),json={'text':msgtext,'callSignNames':[callsign],'transmitterGroupNames':[transmittergrp],'emergency':False})

if req.status_code == 401:
	logger.error('Message could not be sent')
