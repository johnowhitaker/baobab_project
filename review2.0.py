#####################################################################################
# Scans through images              												#
# Click on FOIs    (features of interest)											#
# Saves FOI coords and mini pics    												#
# Right click to tag as unsure            											#
#####################################################################################
#																					#
# Usage: python review2.0.py "/path/to/images/*.png" "Name to save shapefiles as"	#
#																					#
# Author: Jonathan Whitaker <johnowhitaker@yahoo.com>								#
#																					#
#####################################################################################

#requires python-pygame, shapefile.py, goe_convert.py

import pygame, glob, re, shapefile, sys
from geo_convert import *

# Change this to whatever size the images are
image_size = 800

#left hand side menu, <<<re-do if have time
menu_image = pygame.image.load("menu.png")

pictures = []

#Get the command line arguments
path_to_pics = str(sys.argv[1]) #name really says it all
save_name = str(sys.argv[2])    #what to save the shapefiles as

#find the images
picture_files = glob.glob(path_to_pics)

#sort the images
picture_files.sort()#for GPS waypoints: sort((key=lambda x: x[x.find(')'):] )

#Throw an error if no picture files are provided
if len(picture_files) == 0:
	print("Error, no picture files found! deary deary me...")
	
#load the images all at once - improves speed
print("Loading Images...")
for picfile in picture_files:
    pic = pygame.image.load(picfile)
    pictures.append(pic)
print("done")


def main():

    #pygame stuff...
    pygame.init()
    screen = pygame.display.set_mode((900, 800), 0)	# Change this if downloading images of different size (x+100, y)
    clock = pygame.time.Clock()

    positives = []
    maybes = []
    pos_locations = [] #locations of all positives
    may_locations = []
    center_locations = [] #the center of each image done
    unclear_locations = []

    #for the menu
    next_mouseover = False
    save_mouseover = False
    unclear_mouseover = False
    clear_mouseover = False

    img_number = 1

    while img_number < len(pictures):

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_q and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                next_mouseover = False
                save_mouseover = False
                clear_mouseover = False
                unclear_mouseover = False
                if pos[0] < 100:    #in menu
                    if pos[1] > 150 and pos[1] < 240:
                        next_mouseover = True

                    if pos[1] > 260 and pos[1] < 330:
                        save_mouseover = True

                    if pos[1] > 350 and pos[1] < 385:
                        clear_mouseover = True

                    if pos[1] > 420 and pos[1] < 500:
                        unclear_mouseover = True


            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1: # left click for FOI
                    if next_mouseover == True:

                        #show image name
                        pygame.display.set_caption(str(picture_files[(img_number)]))

                        #regular expressions... condensed magic smoke!!!!
                        p = re.compile('\-\d{2}\.\d+|\d{2}\.\d+')
                        #extract the coords from the image name
                        coords = p.findall(picture_files[(img_number-1)])
                        lat, lon = float(coords[0]), float(coords[1])
                        center_locations.append([lat, lon])
                        #iterate through positives and maybes, generating a location for each and storing in pos_locations and may_locations
                        for p in positives:
                            loc = FindLoc((lat, lon), (p[0]-100), p[1], 18)  #nearly missed the -100... crisis averted!
                            pos_locations.append(loc)
                        for m in maybes:
                            loc = FindLoc((lat, lon), (m[0]-100), m[1], 18)
                            may_locations.append(loc)
                        positives = []
                        maybes = []
                        #load next image
                        img_number += 1


                    elif save_mouseover == True:
                        #save positives, maybes, area covered and unclears to shapefiles
                        print("saving to shapefiles")
                        saveShapefile(pos_locations, may_locations, center_locations, unclear_locations)
                  

                    elif clear_mouseover == True:
                        #clear the screen
                        positives = [] #<<<<< allowed this time :)
                        maybes = []
                    elif unclear_mouseover == True:
                        p = re.compile('\-\d{2}\.\d+|\d{2}\.\d+')
                        #extract the coords from the image name
                        coords = p.findall(picture_files[(img_number-1)])
                        lat, lon = float(coords[0]), float(coords[1])
                        unclear_locations.append([lat, lon])

                        #show image name
                        pygame.display.set_caption(str(picture_files[(img_number)]))
                        img_number += 1
                    else:
                        position = event.pos
                        positives = positives + [position]
                        #save a small image of the tree for haartraining
                        #rect = pygame.Rect((position[0]-35), (position[1]-35), 70, 70)
                        #screenshot.blit(screen, (0, 0), rect)
                        #pygame.image.save(screenshot, (str(small_pic_num)+".png"))
                        #print("saved small image: " + str(small_pic_num) + ".png")
                        #small_pic_num += 1


                elif event.button == 3: # right click if unsure
                    position = event.pos
                    maybes = maybes + [position]

        screen.fill((0, 0, 0))
        screen.blit(pictures[(img_number-1)], (100, 0)) #####change back fro image_sizeximage_size images to 100,0

        # draw on positives and maybes
        for positive in positives:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect((positive[0]-35), (positive[1]-35), 70, 70), 2)
        for maybe in maybes:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect((maybe[0]-35), (maybe[1]-35), 70, 70), 1)


        # draw the menu << little sad, but it works
        screen.blit(menu_image, (0, 0))

        #highlight menu item
        if True:
            if next_mouseover == True:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 150, 80, 80), 3)
            if save_mouseover == True:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 253, 80, 80), 3)
            if clear_mouseover == True:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 350, 80, 40), 3)
            if unclear_mouseover == True:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 415, 80, 80), 3)

        pygame.display.flip()

        clock.tick(30)

    #save before exit
    if img_number == len(pictures):
        print("saving to shapefiles")
        saveShapefile(pos_locations, may_locations, center_locations, unclear_locations)

def saveShapefile(pos_locations, may_locations, center_locations, unclear_locations):
	# Make a point shapefile for positives
	w = shapefile.Writer(shapefile.POINT)
	w.field('Lattitude')
	w.field('Longitude','C','40')
	#iterate through positives and add to point file
	for i in range(0, len(pos_locations)):
		lat, lon = pos_locations[i][1], pos_locations[i][0]  #switched by magic smoke?
		w.point(lat, lon)
		w.record(str(lat), str(lon))
	w.save(save_name+"_positives")
	# Make a point shapefile for the maybes
	w = shapefile.Writer(shapefile.POINT)
	w.field('Lattitude','C','40')
	w.field('Longitude','C','40')
	#iterate through maybes and add to point file
	for i in range(0, len(may_locations)):
		lat, lon = may_locations[i][1], may_locations[i][0]  #switched by magic smoke
		w.point(lat, lon)
		w.record(str(lat), str(lon))
	if len(may_locations) == 0:
		#Have to add at least one maybe to stop it throwing an error
		w.point(lat, lon)
		w.record(str(lat), str(lon))
	w.save(save_name+"_maybes")
	#make a polygon shapefile to store area covered
	w = shapefile.Writer(shapefile.POLYGON)
	w.field('Center Lat','C','40')
	w.field('Center Lon','C','40')
	for i in range(0, len(center_locations)):
		lat, lon = center_locations[i][0], center_locations[i][1]
		UR_loc = FindLoc((lat, lon), 0, 0, 18)
		BR_loc = FindLoc((lat, lon), image_size, 0, 18)
		BL_loc = FindLoc((lat, lon), image_size, image_size, 18)
		UL_loc = FindLoc((lat, lon), 0, image_size, 18)
		w.poly(parts=[[[UL_loc[1], UL_loc[0]],[UR_loc[1], UR_loc[0]],[BR_loc[1], BR_loc[0]],[BL_loc[1], BL_loc[0]]]])
		w.record(str(lat), str(lon))
	w.save(save_name+"_area_covered")
	# Make a point shapefile for unclear ones
	w = shapefile.Writer(shapefile.POINT)
	w.field('Lattitude')
	w.field('Longitude','C','40')
	for i in range(0, len(unclear_locations)):
		lat, lon = unclear_locations[i][1], unclear_locations[i][0]  #switched by magic smoke?
		w.point(lat, lon)
		w.record(str(lat), str(lon))
	if len(unclear_locations) == 0:
		lat, lon = -20, 30
		w.point(lat, lon)
		w.record(str(lat), str(lon))
	w.save(save_name+"_unclear")
	
#run the main loop
main()



####
#You'll notice a lot of 1,0 where you'd expect 0,1. There is a lot of flipping back and fourth because frankly I'm a dumbass who forgets the difference
#between lattitude and longitude *actually qgis also swaps them around*. However, The way it is now works, and is accurate. I may change it in the future
#if someone else needs this, but for now.... Si fractum non sit, noli id reficere.
