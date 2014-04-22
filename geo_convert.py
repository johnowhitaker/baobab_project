# A quick module for varios conversions needed when dealing with google earth imagery
# By Jonathan Whitaker, with a bit of code from stack-exchange user Aragon


import Image, urllib, StringIO, random, math

#constants for the images
#make sure these match the ones you use in download_shapefile.py
zoom = 18
xsize = 800
ysize = 800
scale = 2

#some constants
tileSize = 256
initialResolution = 2 * math.pi * 6378137 / tileSize
originShift = 2 * math.pi * 6378137 / 2.0

def LatLonToMeters( lat, lon ):
    "Converts WGS84 lat/lon to spherical mercutor EPSG:900913"
    mx = lon * originShift / 180.0
    my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)
    my = my * originShift / 180.0
    return mx, my


def MetersToPixels( mx, my, zoom):
    "Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"

    res = Resolution( zoom )
    px = (mx + originShift) / res
    py = (my + originShift) / res
    return px, py

def PixelsToMeters( px, py, zoom):
    "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"

    res = Resolution(zoom)
    mx = px * res - originShift
    my = py * res - originShift
    return mx, my

def MetersToLatLon( mx, my ):
    "Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"

    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0

    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
    return lat, lon

def Resolution(zoom):
    res = initialResolution/(2**zoom)
    return res

def FindDistance(Lat1, Lon1, Lat2, Lon2):
    #math.radians() means convert to radians
    d = 6378.137 * math.acos( math.cos( math.radians(Lat1) ) * math.cos( math.radians(Lat2) ) * math.cos( math.radians(Lon2) - math.radians(Lon1) ) + math.sin( math.radians(Lat1) ) * math.sin( math.radians(Lat2) ) )
    return d

def FindLoc(img_center, px, py, zoom):
    clat, clon = img_center[0], img_center[1]
    cmx, cmy = LatLonToMeters( clat, clon )
    cpx, cpy = MetersToPixels( cmx, cmy, zoom)
    cpx -= (200-(px/2))   #double negative. Sue me
    cpy += (200-(py/2))
    mx, my = PixelsToMeters( cpx, cpy, zoom)
    lat, lon = MetersToLatLon(mx, my)
    return lat, lon
        
print("geo_convert successfully imported")
    
