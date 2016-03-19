__author__ = 'KieranMcCool'

import os.path
from fhsa.models import Result
from datetime import date
from sensitivity import get_sensitivity_rating
from apiWrap import *
from django.template.defaultfilters import slugify
import httplib
import pickle

def loadCache():
	if USE_CACHE and os.path.isfile(PICKLE_FILE):
		return pickle.load(open(PICKLE_FILE, "r"))
	return {}

PICKLE_FILE = "cache.pickle"
USE_CACHE = False
cache = loadCache()

def formatURL(s):
        if s[0:8] == "https://":
            return s
        elif s[0:7] == "http://":
            return s
        return "http://" + s

def saveCache():
	pickle.dump(cache, open(PICKLE_FILE, "w+"))

def resetCache():
	cache = {}
	saveCache()

def doSearch(query, api="*", user=None):
	def results(query, api="*", user=None, updateCache = USE_CACHE):
		l = []
		if api == "medline":
			l = medline(query)
		elif api == "healthfinder":
			l = healthfinder(query, user=user)
		elif api == "bing":
			l = bing(query) 
		elif api == "*":
			for api in [ "medline", "healthfinder", "bing" ]:
				l += results(query, api=api, user=user, updateCache = False) 

		if updateCache and api.lower() != "healthfinder":
			cache[query] = [[v for v in l if v["source"].lower() != "healthfinder"] , date.today() ]
			saveCache()

		return l

	def haveCache():
		if not USE_CACHE or api == "healthfinder":
			return False
		return query in cache and (date.today() - cache.get(query)[1]).days < 3
	
	if haveCache():
		l = cache[query][0]
		if api == "*":
			l += results(query, api = "healthfinder", user=user)
		else:
			l = [ q for q in l if q["source"].lower() == api.lower() ]
	else:
		l = results(query, api=api, user=user)

	l.sort(key=lambda x : x["sensitivity"], reverse=True)
	return l

def formatObject(url, title, description, source, shortDescription=""):
	senseData = get_sensitivity_rating(description)
	return { "url":url, "title": title + " (Source: %s)" % source, 
		"description" : description, "source":source, 
		"shortDescription":{True:description, False:shortDescription}[shortDescription == ""],
		"sentimentality": senseData["sentimentality"], "readability": senseData["readability"],
		"sensitivity": senseData["sensitivity"]
		}

def medline(query):
	results = []
	for q in medlineSearch(query):
		
		title = "%s | %s | %s" % (q["groupName"], q["title"], q["organizationName"])		
		url = "medline/?r=%s" % title
		description = q["FullSummary"]

		r = formatObject(url, title, description, "MedLine", shortDescription = q["snippet"])

		results += [r]
	return results

def calculate_age(born):
	today = date.today()
	# Second boolean evaluation casts to 0 or 1 if used as int in python.
	return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def healthfinder(query, user):
	results = []
	return []
	if user == None:
		return []
	for q in hfSearch(query, 
                calculate_age(user.DOB), 
                {"M":"Male","F":"Female"}[user.gender]):

		title = q["Title"]
		url = formatURL(q["AccessibleVersion"])
		description = q["Sections"][0]["Content"]
		
		r = formatObject(url, title, description, "HealthFinder")

		results += [r]
	return results

def bing(query):
	results = []
	for q in bingSearch(query):
		title = q["Title"]
		description = q["Description"]
		url = formatURL(q["DisplayUrl"])

		r = formatObject(url, title, description, "Bing")

		results += [r]
	return results
