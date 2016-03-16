__author__ = 'KieranMcCool'

import os.path
from fhsa.models import Result
from datetime import date
from sensitivity import get_sensitivity_rating
from apiWrap import *
from django.template.defaultfilters import slugify

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

def loadCache():
	if os.path.isfile("cache.pickle"):
		searchCache = pickle.load("cache.pickle")
	else:
		f = open("cache.pickle", "w+")
		f.write("")
		f.close()
		searchCache = {}

def doSearch(query, api="*", user=None):

	if api == "medline":
		return medline(query)
	elif api == "healthfinder" and user != None:
		return healthfinder(query)
	elif api == "bing":
		return bing(query)
	elif api == "*":
		print "nyi"
	return []

"""
    apiDict = { 
        "ml": lambda x :[["", "%s | %s | %s (Source: Medline)" % (q["groupName"], q["title"], q["organizationName"]), 
             ] for q in medlineSearch(x) ],
        "bs": lambda x : [[formatURL(q["DisplayUrl"]), 
            formatURL(q["DisplayUrl"]) + " (Source: Bing)", q["Description"]] for q in bingSearch(x)],  
        "hf": lambda x : {False:lambda x : [],True:lambda x : [[formatURL(q["AccessibleVersion"]),  # I'm so sorry for this... (With love from Kieran <3)
            q["Title"] + " (Source : HealthFinder)", q["Sections"][0]["Content"] ] for q in hfSearch(x, 
                int((date.today() - user.DOB).days / 365.2425), {"M":"Male","F":"Female"}[user.gender])]}[logged](x),
        "*" : lambda x : apiDict["ml"](x) + apiDict["hf"](x) + apiDict["bs"](x)
    }

   """

def medline(query):
	results = []
	for q in medlineSearch(query):
		title = "%s | %s | %s" % (q["groupName"], q["title"], q["organizationName"])		
		url = "medline/%s" % slugify(title)

		try:
			r = Result.objects.get(url=url)
		except:
			r = Result.objects.create(url=url)

		r.title = title
		r.description = q["FullSummary"]
		r.source = "medline"
		url = ""
		senseData = get_sensitivity_rating(q["FullSummary"])
		r.sentimentality = senseData["sentimentality"]
		r.readability = senseData["readability"]
		r.sensitivity = senseData["sensitivity"]
		results += [r]
	return results

def healthfinder(query, user):
	print "nyi"

def bing(query):
	results = []
	for q in bingSearch(query):
		title = formatURL(q["DisplayUrl"]) + " (Source: Bing)"		
		url = formatURL(q["DisplayUrl"])

		try:
			r = Result.objects.get(url=url)
		except:
			r = Result.objects.create(url=url)

		r.title = title
		r.description = q["Description"]
		r.source = "bing"
		senseData = get_sensitivity_rating(q["Description"])
		r.sentimentality = senseData["sentimentality"]
		r.readability = senseData["readability"]
		r.sensitivity = senseData["sensitivity"]
		results += [r]
	return results
	