Baobab Project Utilities
========================

Various tools related to the resource assesment of baobabs in Zimbabwe.

To install dependancies in Ubuntu:
  sudo apt-get install qgis python-pygame python-sklearn python-imaging
  
Tools:

1) download_shapefile.py - downloads images from Google's static maps server for each point in a shapefile.
    Usage: python download_shapefile.py "path/to/shapefile"
                          
2) geo_convert.py - methods used in other programs, not intended to be used on its own

3) shapefile.py - library for reading shapefiles (not my code - see http://code.google.com/p/pyshp/)

4) review.py - go through the images aquired with download_shapefile.py, click to tag a baobab, right click for unsure.
    Usage: python review2.0.py "/path/to/images" "shapefile_name_to_save_as"
    e.g. python review2.0.py 'sample data/*.png' 'test_review'

5) rforest.py - build a model based on one shapefile, make a prediction for each point in a different shapefile and save this prediction to a new shapefile. Edit the various paths in the program then run with 'python rforest.py'
