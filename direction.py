import requests
import pandas as pd
import numpy as np
import csv

#improvement: search for coffee shops and then food
#also search by number of checkins

#takes desired lat/lng, returns json object with all the things
#cat id must be complete string of ids (eg, '4d4b7105d754a06374d81259, 4d4b7105d754a06374d81259')
def getVenues(metrolat, metrolng, radius, catId):
	url = "https://api.foursquare.com/v2/venues/search?client_id=UZWX53LQSWRFMDH5IIXMXAE4NJ411PANC05LVDJJGWC0SUPQ&client_secret=B5WVERK33CNB3NDD0UODLC3FBODFUYIBWT5F0A3PMKS1ZGIQ&v=20130815&ll=" + str(metrolat) + "," + str(metrolng) + "&intent=checkin&radius=" + str(radius) + "&categoryId=" + str(catId)
	response = requests.get(url).json()
	return response

#for index, item in enumerate(response['response']['venues'][0]['location']):
#	print "{0}: {1}".format(index, item)

# latitude = response['response']['venues'][0]['location']['lat']
# longitude = response['response']['venues'][0]['location']['lng']

# #testing to see if we got latitude/longtitude
# #print "{0}, {1}".format(latitude, longitude)

# #testing to see if north or south
# if longitude > 38.9086828861285:
# 	print "This is north."
# elif longitude < 38.9086828861285:
# 	print "This is south."
# else:
# 	print "This is in the metro station."

# #testing for east or west
# if latitude > -77.0433192930102:
# 	print "This is east."
# elif latitude < -77.0433192930102:
# 	print "This is west."
# else:
# 	print "This is in the metro station."

#print out list of things
# for index, item in enumerate(response['response']['venues']):
# 	print "{0}: {1} \n {2}, {3}".format(index, item['name'], item['location']['lat'], item['location']['lng'])

#input: json object of venue info from foursquare api / output: lists of venues in different directions
def parseVenues(response, metrolat, metrolng):
	#make list of venues with venue name + lat/lng
	venues = {}

	for item in response['response']['venues']:
		venues[item['name']] = {'lat' : item['location']['lat'], 'lng' : item['location']['lng']}

	#create list of empty directional lists; we are going to put the name of landmark into each of these lists after checking directions
	north = []
	south = []
	east = []
	west = []
	northeast = []
	northwest = []
	southeast = []
	southwest = []

	for key, item in venues.items():
		#test for north/test for south
		if abs(item['lat'] - metrolat) < .00001:
			if item['lat'] > metrolat:
				#north
				north.append(key)
			elif item['lat'] < metrolat:
				#south
				south.append(key)
		#test for east/test for west
		elif abs(item['lng'] - metrolng) < .00001:
			if item['lng'] > metrolng:
				east.append(key)
			elif item['lng'] < metrolng:
				west.append(key)

		#test for northeast/test for southeast
		elif item['lng'] > metrolng:
			if item['lat'] > metrolat:
				#northeast
				northeast.append(key)
			elif item['lat'] < metrolat:
				#southeast
				southeast.append(key)
		#test for northwest/test for southwest
		elif item['lng'] < metrolng:
			if item['lat'] > metrolat:
				#nortwest
				northwest.append(key)
			elif item['lat'] < metrolat:
				#southwest
				southwest.append(key)
	final = {'north':north, 'south':south, 'east': east, 'west':west, 'northeast':northeast, 'southeast':southeast, 'northwest':northwest, 'southwest':southwest}
	return final

# for key, item in venues.items():
# 	print "{0} : {1}".format(key,item)

# print "North: {0}".format(north)
# print "south: {0}".format(south)
# print "east: {0}".format(east)
# print "west: {0}".format(west)
# print "Northeast: {0}".format(northeast)
# print "southeast: {0}".format(southeast)
# print "northwest: {0}".format(northwest)
# print "southwest: {0}".format(southwest)

##test function
def importMetro(metrofile):
	metros = pd.read_csv(metrofile)
	return(metros)

metros_df = importMetro('metros.csv')
columns = ["lat", "lng", "metro", "exit", "venues"]
# export_df = pd.DataFrame(columns=columns)

# print export_df.head()

radius = 20
catId = '4d4b7105d754a06374d81259,4d4b7104d754a06370d81259'
export = {}

for index, row in metros_df.iterrows():
	response = getVenues(row['lat'], row['lng'], radius, catId)
	directions = parseVenues(response,row['lat'], row['lng'])

	final = []
	for key,item in directions.iteritems():
		if item:
			final.append(item)
	#print "metro: {0} \n exit: {1} \n venues: {2}".format(row['metro'], row['exit'], final)
	#metros_df.loc[row,'venues'] = final
	newline = {'lat': row['lat'], 'lng': row['lng'], 'metro': row['metro'], 'exit': row['exit'], 'venues' : final}
	export[str(index)] = newline

writer = csv.writer(open('allthemetros.csv','wb'))
for key, value in export.items():
   writer.writerow([key, value])

# metrolat = 38.90868289
# metrolng = -77.04331929
# radius = 20

# response = getVenues(metrolat, metrolng, radius)
# directions = parseVenues(response)

# print directions
