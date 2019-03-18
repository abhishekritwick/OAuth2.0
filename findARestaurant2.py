from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "K2RZOR2LIJAFTO4RILMEN2XMVITIELTEG25REO2CKWWGPZS0"
foursquare_client_secret = "FOPMRIDGHNMSW0JX4XRX1XHJ4HUB104OKEJCNIX5W51SJSWZ"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
	h = httplib2.Http()
	restaurant = json.loads(h.request(url,'GET')[1])
	venue_id = restaurant['response']['venues'][0]['id']
	restaurant_name = restaurant['response']['venues'][0]['name']
	restaurant_address = restaurant['response']['venues'][0]['location']['formattedAddress']
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	if venue_id:
		imageAPIurl = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20130815' % (venue_id, foursquare_client_id, foursquare_client_secret))
		h2 = httplib2.Http()
		imgresult = json.loads(h2.request(imageAPIurl, 'GET')[1])
		if imgresult['response']['photos']['items']:
			first_pic = imgresult['response']['photos']['items'][0]
			prefix = first_pic['prefix']
			suffix = first_pic['suffix']
			imageURL = prefix + "300x300" + suffix
		else:
			imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
		print "Restaurant Name %s" % restaurant_name
		print "Restaurant Address %s" % restaurant_address
		print "Restaurant Image %s \n" % imageURL
		return restaurantInfo

	else:
		print " No restaurants found for %s location" %location
		return "No Restaurants Found"
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")
