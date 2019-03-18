from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




foursquare_client_id = 'K2RZOR2LIJAFTO4RILMEN2XMVITIELTEG25REO2CKWWGPZS0'
foursquare_client_secret = 'FOPMRIDGHNMSW0JX4XRX1XHJ4HUB104OKEJCNIX5W51SJSWZ'
google_api_key = 'AIzaSyDp1YtEwo3wuJ-oSjuyql80f0-Ur-OrAEU'

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  if request.method == 'GET':
      showAllRestaurants()
  elif request.method == 'POST':
      location = request.args.get('location', '')
      mealType = request.args.get('mealType','')
      restaurantInfo = findARestaurant(mealType,location)
      makeARestaurant(restaurantInfo)


@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  if request.method == 'GET':
      showRestaurantDetails(id)
  if request.method == 'PUT':
      name = request.args.get('name','')
      location = request.args.get('address','')
      image = request.args.get('image','')
      updateRestaurant(id,name,location,image)
  if request.method == 'DELETE':
      deleteRestaurant(id)


def showAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants = [rest.serialize for rest in restaurants])

def showRestaurantDetails(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    return jsonify(restaurant = restaurant.serialize)

def makeARestaurant(restaurantInfo):
    if restaurantInfo != "No Restaurants Found":
        name = unicode(restaurantInfo['name'])
        address = unicode(restaurantInfo['address'])
        image = unicode(restaurantInfo['image'])
        restaurant = Restaurant(restaurant_name = name,restaurant_address = address, restaurant_image = image)
        session.add(restaurant)
        session.commit()
        return jsonify(restaurant = restaurant.serialize)
    else:
        return jsonify({"error":"No Restaurants Found for %s in %s" %(mealType,location)})

def updateRestaurant(id,name,location,image):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    if name:
        restaurant.restaurant_name = name
    if location:
        restaurant.restaurant_address = location
    if image:
        restaurant.restaurant_image = image
    session.add(restaurant)
    session.commit()
    return jsonify(restaurant = restaurant.serialize)

def deleteRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    session.delete()
    session.commit()
    return jsonify({"message":"Restaurant Deleted"})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
