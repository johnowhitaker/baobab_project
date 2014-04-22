#!/usr/bin/python

#TODO: Remove API key before publishing

# Saves images from Google's static maps server for each point in a shapefile
# Run from command line 'python download_shapefile.py "path/to/shapefile"'
# By Jonathan Whitaker

# requires shapefile.py (pyshp) and python-imaging (PIL) libraries, and geo_convert.py

import shapefile, sys, Image, urllib, StringIO, random, math
from geo_convert import *

#load in the shape file, get a list of coordinates
try:
	sf = shapefile.Reader(str(sys.argv[1]))
except:
	print "Please provide a valid shapefile"
shapes = sf.shapes()
coords = []
records = sf.records()
for i in range(0, len(shapes)):
	coords.append(shapes[i].points[0])

#constants for the images - see googles maps api
zoom = 18
xsize = 800
ysize = 800
scale = 2

#change this if restarting after downloading some images
img_number = 1

#through the rows
for i in range((img_number-1), (len(coords))):
	#grab a static image from google
	lat, lon = coords[i][1],coords[i][0]	#lat/lon, these are switched by some GIS programs and may need reversing
	position = ','.join((str(lat), str(lon)))
	urlparams = urllib.urlencode({'center': position,
						'zoom': str(zoom),
						'size': '%dx%d' % (xsize, ysize),
						'maptype': 'satellite',
						'sensor': 'false',
						'scale': scale,
						'key': "AIzaSyDJZrNZ2vQ_L3_A6TqbJUNaZwj0cKxlsLQ"})
	url = 'http://maps.google.com/maps/api/staticmap?' + urlparams
	im_name = "img_"+str(img_number)+"(" + str(lat)+";"+str(lon)+")"
	print("downloading " + im_name)
	f=urllib.urlopen(url)
	im=Image.open(StringIO.StringIO(f.read()))
	print("saving "+im_name +".png")
	im.save(im_name+".png")
	img_number += 1

