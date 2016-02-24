# Identiji generator
# Kieran McCool (2142393)

# THIS PYTHON MODULE REQUIRE THE PYTHON IMAGING LIBRARY, RUN "pip install pillow" TO GET THIS.

from math import pow
import random
from PIL import Image, ImageDraw

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

def finalHash(name):
	# This is formats the hash correctly, if getting hashes, use this.
	return addZeroes(format(abs(getHash(name)), "x"), 8)[:8]


def genImage(unhash, hash):
	global size, blocks
	col = ( int(hash[0:2], 16), int(hash[2:4], 16), int(hash[4:6], 16), 255 )
	random.seed(int(hash[6:8], 16))

	img = Image.new("RGBA", (size * 10 , size * 10), (240,240,240,255))
	drawer = ImageDraw.Draw(img)

	mult = size/((blocks*2)-1);
	for x in range(0, blocks):
		for y in range(0, blocks * 2):
			if random.randint(0, 10) > 5:
				drawer.rectangle([ (x*mult, y*mult), (mult, mult) ], fill = col)
				drawer.rectangle([ (size - (x+1) * mult, y*mult), (mult, mult) ], fill = col)

	img.save(unhash + ".png", "PNG")

while True:
        name = raw_input("Name:- ")
        hs = finalHash(name)
        print "Hash:-  " + hs
        genImage(name, hs)
        print "%s.png saved in this directory." % name

        
