medlineKey = ""
hfKey = ""
bingKey = ""

def medlineSearch():
	return "nyi"

def bingSearch():
	return "nyi"

def hfSearch():
	return "nyi"

def urlBuilder(dict):
	out = "?" + dict.keys()[0] + "=" + dict[dict.keys()[0]]

	for i in range(len(dict.keys())):
		out += "&%s=%s" % ( dict.keys()[i], dict[dict.keys()[i]] ) 
	return out

print urlBuilder({ "query":"toast is good", "user":"Kieran McCool" })