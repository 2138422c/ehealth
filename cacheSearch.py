__author__ = 'KieranMcCool'

import os.path
from fhsa.models import Result
from datetime import date
from sensitivity import get_sensitivity_rating
from apiWrap import *
from django.template.defaultfilters import slugify
import httplib


def titleFromHtml(url):
	request = urllib2.urlopen(url)
	response = request.read()
	tt = response.split('<title>')[1]
	title = tt.split('</title>')[0]
	return title

def calculate_age(born):
    today = date.today()
    # Second boolean evaluation casts to 0 or 1 if used as int in python.
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def formatURL(s):
        if s[0:8] == "https://":
            return s
        elif s[0:7] == "http://":
            return s
        return "http://" + s

def doSearch(query, api="*", user=None):

	if api == "medline":
		l = medline(query)
	elif api == "healthfinder" and user != None:
		l = healthfinder(query, user=user)
	elif api == "bing":
		l = bing(query)
	elif api == "*":
		l = medline(query) + healthfinder(query, user=user)  + bing(query)
	l.sort(key=lambda x : x.sensitivity, reverse=True)
	return l

def formatObject(url, title, description, source):
		try:
			r = Result.objects.get(url=url)
		except:
			r = Result.objects.create(url=url)

		r.title = title + " (Source: %s)" % source
		r.description = description
		r.source = source
		senseData = get_sensitivity_rating(description)
		r.sentimentality = senseData["sentimentality"]
		r.readability = senseData["readability"]
		r.sensitivity = senseData["sensitivity"]
		r.retrieved = date.today()

		return r

def medline(query):
	results = []
	for q in medlineSearch(query):
		
		title = "%s | %s | %s" % (q["groupName"], q["title"], q["organizationName"])		
		url = "medline/?r=%s" % title
		description = q["FullSummary"]

		r = formatObject(url, title, description, "MedLine")

		results += [r]
	return results

def healthfinder(query, user):
	results = []
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

		url = formatURL(q["DisplayUrl"])
		try:
			title = titleFromHtml(formatURL(url))		
		except:
			title = formatURL(q["DisplayUrl"])
		description = q["Description"]

		r = formatObject(url, title, description, "Bing")

		results += [r]
	return results
	