# Identiji generator
# Kieran McCool (2142393)

# THIS PYTHON MODULE REQUIRE THE PYTHON IMAGING LIBRARY, RUN "pip install pillow" TO GET THIS.

from math import pow
import random
import os
from PIL import Image, ImageDraw
import StringIO

# Output avatars will be SIZExSIZE pixels
SIZE = 800
# Each quadrant of the image is BLOCKSxBLOCKS
BLOCKS = 7

def getHash(s):
	# init hash as 0
	hash = 0
	# foreach character
	for c in s:
		# get char code
		char = ord(c)
		# left bitshift hash 5 times, subract hash and add on the character code.
		hash = ((hash << 5) - hash) + char
	return hash

def addZeroes(n, x):
	# if hash produced is less than x digits long, append 0s to front as place holder
	for i in range(0, x - len(n)):
		n = "0" + n
	return n

def finalHash(name):
	# This is formats the hash correctly, if getting hashes, use this.
	return addZeroes(format(abs(getHash(name)), "x"), 8)[:8]


def genImage(outPath, hash):
	global SIZE, BLOCKS

	# Colour is a tuple in format (R, G, B, a) - populated by hash data
	col = ( int(hash[0:2], 16), int(hash[2:4], 16), int(hash[4:6], 16), 255 )
	# Seed random generator with hash data
	random.seed(int(hash[6:8], 16))

	# Generate a new image of size and with an almost white background
	img = Image.new("RGBA", (SIZE, SIZE), (240,240,240,255))
	drawer = ImageDraw.Draw(img)

	# Each block will be blockSize x blockSize pixels
	blockSize = SIZE/BLOCKS/2

	# draws a block.
	def offsetRect(x, y, c):
		# This just calculates the offsets, if we try to fill the whole image
		# then we end up with uneven parts where a little bit runs off the edge
		# or symetry isn't guaranteed.
		if x > BLOCKS/2:
			xCoord = x * blockSize - (BLOCKS % SIZE)
		else:
			xCoord = x * blockSize + (BLOCKS % SIZE)
		if y > BLOCKS/2:
			yCoord = y * blockSize - (BLOCKS % SIZE)
		else:
			yCoord = y * blockSize + (BLOCKS % SIZE)
			
		# fill the block at desired location.
		drawer.rectangle([(xCoord, yCoord),
			(xCoord + blockSize, yCoord + blockSize)], fill = c)
	# For each x block
	for x in range(0, BLOCKS):
		# foreach y block
		for y in range(0, BLOCKS * 2):
			# If hash generates an integer > 5 (50% chance of colouring each square)
			if random.randint(0, 10) > 5:
				# Colour the block and it's counterpart on the other half for rotational symetry.
				offsetRect(x,y,col)
				offsetRect((2*BLOCKS) - (x + 1),y,col)
	fileout = os.path.join(outPath, hash + ".jpeg")
	img.save(fileout, "jpeg")
	imgAsString = open(fileout).read()
	return fileout

# This method is the one we use!!!!!!!
def generateAvatar(name, outPath):
        # gets a properly formatted hash
        hash = finalHash(name)
        # Makes sure the location we're saving to exists.
        pathMinusFileName = os.path.dirname(os.path.realpath(outPath))
        # if not, creates it
        if not os.path.exists(pathMinusFileName):
        	os.mkdir(pathMinusFileName)
        # Generates the image to the desired location
        return genImage(outPath, hash)

def sample():
	# This sample method shows how you use the generateAvatar method.
	for s in [ "Kieran McCool", "Lewis Boyd", "Alistair Cross", "Ryan Fox" ]:
		generateAvatar(s, os.path.join(os.path.dirname(os.path.realpath(__file__)), "avatars/" , s + ".png"))


        
