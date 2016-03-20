import urllib2
from django.template.defaultfilters import slugify
import json
import xml.etree.ElementTree as ET
import re

hfKey = "dbhhdqjgwwbigtwk"
bingKey = "d0yoBORYWMf3D7h5lT8Bum8iLRnhJg3UFNBQjD636gc"

def queryFormat(s):
	return "%%27%s%%27" % slugify(s)

def stripHtml(s):
	return re.sub('<[^>]*>', '', s)

def medlineSearch(term, debug=False):

	if debug:
		return testML(term)

	base = "https://wsearch.nlm.nih.gov/ws/query"
	base = urlBuilder(base, { "db":"healthTopics", "term":queryFormat(term)})

	request = urllib2.urlopen(base)
	results = ET.fromstring(request.read())

	out = []

	for document in results.iter('document'):
			out += [{ content.attrib["name"]: content.text for content in document.iter("content") }]

	for d in out:
		for k in d.keys():
			d[k] = stripHtml(d[k])

	return out

def bingSearch(term, debug=False):

	if debug:
		return testBing(term)

	credentialBing = 'Basic ' + (':%s' % bingKey).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds

	top = 20

	url = 'https://api.datamarket.azure.com/Bing/Search/Web'
	url = urlBuilder(url, {"Query":queryFormat(term), "$top":top, "$format":"json"})

	request = urllib2.Request(url)
	request.add_header('Authorization', credentialBing)
	requestOpener = urllib2.build_opener()
	response = requestOpener.open(request) 

	results = json.load(response)["d"]["results"]

	return results


def hfSearch(term, age, gender, who="someone", pregnant=0, debug=False):
	def hfSillyFormatting(s):
		l = s.split(" ")
		out = "%%22%s" % l[0]
		for i in range(1, len(l)):
			out += "%%20%s" % (l[i])
		return out + "%22"

	if debug:
		return testHF(term, age, gender, who=who, pregnant=pregnant)

	base = "http://healthfinder.gov/developer/Search.json"
	base = urlBuilder(base, { "keyword":hfSillyFormatting(term), "gender":gender,
	 "age":age, "who":who, "pregnant":pregnant, "api_key":hfKey })

	request = urllib2.urlopen(base)
	response = request.read()
	results = json.loads(stripHtml(response))["Result"]

	if results["Total"] == "0":
		return []
	return results["Topics"]

def urlBuilder(baseUrl, dict):
	out = "?%s=%s" % (dict.keys()[0], dict[dict.keys()[0]])

	for i in range(1, len(dict.keys())):
		out += "&%s=%s" % ( dict.keys()[i], dict[dict.keys()[i]] ) 
	return baseUrl + out

def testBing(query):
	d =  bingSearch(query) 
	f = open("testBing.txt", "w+")
	for r in d:
		f.write("\n%s\n" % r)
	return d

def testML(query):
	d = medlineSearch(query)
	f = open("testMedLine.txt", "w+")
	for i in d:
		f.write(str(i) + "\n\n")
	return d

def testHF(query, age, gender, who="someone", pregnant=0):
	f = open("testHealthFinder.txt", "w+")
	d = hfSearch(query, age, gender, who=who, pregnant=pregnant)
	f.write(str(d))
	return d