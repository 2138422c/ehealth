from math import pow
from random import randint

size = 400
blocks = 3

def getHash(s):
	hash = 0
	for c in s:
		char = ord(c)
		hash = ((hash << 5) - hash) + char
	return hash

def addZeroes(n, x):
	for i in range(0, x - len(n)):
		n = "0" + n
	return n

def genImage():
        

while True:
        name = raw_input("Name:- ")
        hs = addZeroes(format(abs(getHash(name)), "x"), 8)[:8]
        print "Hash:-  " + hs

        
