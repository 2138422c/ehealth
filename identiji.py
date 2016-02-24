# Identiji generator
# Kieran McCool (2142393)

# THIS PYTHON MODULE REQUIRE THE PYTHON IMAGING LIBRARY, RUN "pip install pillow" TO GET THIS.

from math import pow
import random
import os
from PIL import Image, ImageDraw

size = 600
blocks = 7

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


def genImage(outFile, hash):
	global size, blocks

	col = ( int(hash[0:2], 16), int(hash[2:4], 16), int(hash[4:6], 16), 255 )
	random.seed(int(hash[6:8], 16))

	img = Image.new("RGBA", (size, size), (240,240,240,255))
	drawer = ImageDraw.Draw(img)

	blockSize = size/blocks/2

	def offsetRect(x, y, c):
		drawer.rectangle([(x * blockSize, y * blockSize),
			(x * blockSize + blockSize, y * blockSize + blockSize)], fill = c)

	for x in range(0, blocks):
		for y in range(0, blocks * 2):
			if random.randint(0, 10) > 5:
				offsetRect(x,y,col)
				offsetRect((2*blocks) - (x + 1),y,col)


	img.save(outFile, "PNG")




# This method is the one we use!!!!!!!
def generateAvatar(name, outPath):
        hash = finalHash(name)
        pathMinusFileName = os.path.dirname(os.path.realpath(outPath))
        if not os.path.exists(pathMinusFileName):
        	os.mkdir(pathMinusFileName)
        genImage(outPath, hash)

for s in [ "Kieran McCool", "Lewis Boyd", "Alistair Cross", "Ryan Fox" ]:
	generateAvatar(s, os.path.join(os.path.dirname(os.path.realpath(__file__)), "avatars/" , s + ".png"))

        
