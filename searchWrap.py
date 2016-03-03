import urllib2
from django.template.defaultfilters import slugify
import json

hfKey = "dbhhdqjgwwbigtwk"
bingKey = "d0yoBORYWMf3D7h5lT8Bum8iLRnhJg3UFNBQjD636gc"

def webContent(url):
	print url
	file = urllib2.urlopen(url)
	data = file.read()
	file.close()
	return str(data)

def medlineSearch(term):
	base = "https://wsearch.nlm.nih.gov/ws/query"
	return "nyi"

def bingSearch(query):
	credentialBing = 'Basic ' + (':%s' % bingKey).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
	def sillyBingFormatting(s):
		return "%%27%s%%27" % slugify(s)

	top = 20

	url = 'https://api.datamarket.azure.com/Bing/Search/Web'
	url = urlBuilder(url, {"Query":sillyBingFormatting(query), "$top":top, "$format":"json"})

	print url

	request = urllib2.Request(url)
	request.add_header('Authorization', credentialBing)
	requestOpener = urllib2.build_opener()
	response = requestOpener.open(request) 

	results = json.load(response)["d"]["results"]

	return results


def hfSearch(term):
	base = "http://healthfinder.gov/developer/Search.xml"
	return "nyi"

def urlBuilder(baseUrl, dict):
	out = "?%s=%s" % (dict.keys()[0], dict[dict.keys()[0]])

	for i in range(1, len(dict.keys())):
		out += "&%s=%s" % ( dict.keys()[i], dict[dict.keys()[i]] ) 
	return baseUrl + out

#print urlBuilder("www.kieranisgod.com", { "query":"toast is good", "user":"Kieran McCool" })

d =  bingSearch("Toast and beans") # I was eating those at the time of writing.
f = open("test", "w+")
for r in d:
	f.write("\n%s\n" % r)