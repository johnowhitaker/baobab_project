import numpy as np
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt
#!/usr/bin/python
import sqlite3
import shapefile
import random
import urllib, StringIO, re, warnings
warnings.filterwarnings("ignore") #removes the deprecation warnings

#load the shapefile into an array (plots2)
print "Loading shapefile..."	
shpfl = shapefile.Reader("/home/jonathan/Baobab/data/Final/final_training")
geomet = shpfl.shapeRecords()
shapes = shpfl.shapes()

plots = []
for shp in range(0, len(geomet)):
	attributes = geomet[shp].record
	plots.append(attributes)
inputs = []
values = []

for i in range(0, len(plots)):
	plot = plots[i]
	inputs.append(plot[2:]) #all the different factors
	values.append(plot[0]) #the number of trees

X = np.array(inputs)
y = np.array(values)
print "Initializing Random Forest Regressor"
regressor = RandomForestRegressor(n_estimators=150, min_samples_split=1, compute_importances=True)
regressor.fit(X, y)
print regressor.feature_importances_ #The weights of each factor


print "loading shapefile"
#load the shapefile containing points for which we will make a prediction
shpfl = shapefile.Reader("/home/jonathan/Baobab/data/zim0092f")
geomet = shpfl.shapeRecords()
shapes = shpfl.shapes()
plots_zim = []
lon = []
lat = []
for shp in range(0, len(geomet)):
	attributes = geomet[shp].record
	details = attributes[1:] #all the different factors
	plots_zim.append(details)
	lat.append(shapes[shp].points[0][1])
	lon.append(shapes[shp].points[0][0])

		
print "Calculating predictions"
results = regressor.predict(plots_zim)
print "Total", sum(results)


total = 0
print "loading landuses shapefile..."
shpfl = shapefile.Reader("/home/jonathan/Baobab/GIS/Landuses/landuses_ignored")
geomet = shpfl.shapeRecords()
shapes = shpfl.shapes()
area = 39058000
for shp in range(0, len(geomet)):
	attributes = geomet[shp].record
	area -= (attributes[0]*10000)
for r in results:
	total += r/4
estimated_total = (total/len(results)*area)
print "Total baobabs:", str(estimated_total)


def save_shapefile(shapename):
	# Save as a shapefile
	print "saving shapefile..."
	w = shapefile.Writer(shapefile.POINT)
	w.field('Predicted Density')
	values = []
		

	for i in range(0, len(lat)):
		lattitude, longitude = lat[i], lon[i]
		w.point(longitude, lattitude)
		w.record(results[i])
	w.save(shapename)

save_shapefile("final_prediction")

def show_results():
	#plot results
	plt.scatter(lon, lat, c=results)#)
	plt.colorbar()
	##plt.gray()
	plt.show()

show_results()

		 
