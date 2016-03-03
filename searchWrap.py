import urllib2
from django.template.defaultfilters import slugify
import json
import xml.etree.ElementTree as ET
import re

hfKey = "dbhhdqjgwwbigtwk"
bingKey = "d0yoBORYWMf3D7h5lT8Bum8iLRnhJg3UFNBQjD636gc"

def queryFormat(s):
	return "%%27%s%%27" % slugify(s)

def medlineSearch(term):
	base = "https://wsearch.nlm.nih.gov/ws/query"
	base = urlBuilder(base, { "db":"healthTopics", "term":queryFormat(term)})

	request = urllib2.urlopen(base)
	results = ET.fromstring(request.read())

	out = []

	for document in results.iter('document'):
			out += [{ content.attrib["name"]: content.text for content in document.iter("content") }]

	return out

def bingSearch(term):
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


def hfSearch(term, age, gender, who="someone", pregnant=0):
	def hfSillyFormatting(s):
		out = ""
		for i in s.split(" "):
			out += "%%22%s" % i
		out += "%22"
		return out
	def stripHtml(s):
		return re.sub('<[^>]*>', '', s)

	base = "http://healthfinder.gov/developer/Search.json"
	base = urlBuilder(base, { "keyword":hfSillyFormatting(term), "gender":gender,
	 "age":age, "who":who, "pregnant":pregnant, "api_key":hfKey })

	request = urllib2.urlopen(base)
	response = request.read()
	results = json.loads(stripHtml(response))["Result"]
	return results

def urlBuilder(baseUrl, dict):
	out = "?%s=%s" % (dict.keys()[0], dict[dict.keys()[0]])

	for i in range(1, len(dict.keys())):
		out += "&%s=%s" % ( dict.keys()[i], dict[dict.keys()[i]] ) 
	return baseUrl + out

#print urlBuilder("www.kieranisgod.com", { "query":"toast is good", "user":"Kieran McCool" })
def testBing():
	d =  bingSearch("Toast and beans") # I was eating those at the time of writing.
	f = open("testBing.txt", "w+")
	for r in d:
		f.write("\n%s\n" % r)

def testML():
	d = medlineSearch("chronic diarrhea")
	f = open("testMedLine.txt", "w+")
	for i in d:
		f.write(str(i) + "\n\n")

def testHF():
	f = open("testHealthFinder.txt", "w+")
	d = hfSearch("Pain", 19, "male")
	f.write(str(d))
#	for k in d.keys():
#		f.write("%s:\n\n\n\t%s" % (k, d[k]))

testBing(); testML(); testHF()