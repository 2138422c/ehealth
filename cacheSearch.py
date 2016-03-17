__author__ = 'KieranMcCool'

import os.path
from fhsa.models import Result
from datetime import date
from sensitivity import get_sensitivity_rating
from apiWrap import *
from django.template.defaultfilters import slugify
import httplib

USE_CACHE = True
cache = { }

def formatURL(s):
        if s[0:8] == "https://":
            return s
        elif s[0:7] == "http://":
            return s
        return "http://" + s

def doSearch(query, api="*", user=None):
	def results(query, api="*", user=None):
		l = []
		if api == "medline":
			l = medline(query)
		elif api == "healthfinder":
			l = healthfinder(query, user=user)
		elif api == "bing":
			l = bing(query) 
		elif api == "*":
			for api in [ "medline", "healthfinder", "bing" ]:
				l += results(query, api=api, user=user) 

		l.sort(key=lambda x : x["sensitivity"], reverse=True)

		if USE_CACHE:
			cache[query] = [ l, date.today() ]

		return l

	def haveCache():
		if not USE_CACHE:
			return False
		return query in cache and (date.today() - cache.get(query)[1]).days < 3
	if haveCache():
		return cache[query][0]
	else:
		return results(query, api=api, user=None)

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
	for q in medlineSearch(query, debug=True):
		
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
	if user == None:
		return []
	for q in hfSearch(query, 
                calculate_age(user.DOB), 
                {"M":"Male","F":"Female"}[user.gender]):

		title = q["Title"] + " (Source : HealthFinder)"		
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
	