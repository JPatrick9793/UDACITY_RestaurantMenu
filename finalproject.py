from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()




# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'}, {'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza', 'description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# *** HOMEPAGE ***
# show all restaurants
@app.route('/')
@app.route('/restaurant')
@app.route('/restaurants')
def showRestaurants():
	# return "This page will show all my restaurants"
	return render_template('restaurants.html', restaurants = restaurants)


# create new restaurant
@app.route('/restaurant/new')
def newRestaurant():
	if request.method == 'POST':
		# total is number of last Restaurant ID
		total = session.query(restaurants).count()
		
		# create new restaurant entry
		newRestaurant = restaurants(name = request.form['name'], id = total + 1)
		
		# add to the session and commit
		session.add(newRestaurant)
		session.commit()
		
		# redirect to homepage
		return redirect(url_for('showRestaurants'))

	else:		
		# direct user to page for creating new restaurants
		return render_template('newRestaurant.html')


# edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	restaurant = restaurants [restaurant_id - 1]
	return render_template('editRestaurant.html', restaurant = restaurant)


# delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	# return "This page will be for deleting a particular restaurant"
	restaurant = restaurants [restaurant_id - 1]
	return render_template('deleteRestaurant.html', restaurant = restaurant)

# show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	# return "This page will show a particular restaurant's menu"
	return render_template('menu.html', items = items, restaurant = restaurant)

# create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return render_template('newMenuItem.html', restaurant = restaurant)

# edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	restaurant = restaurants [restaurant_id - 1]
	item = items [menu_id - 1]
	return render_template('editMenuItem.html', item = item, restaurant = restaurant)

# delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	return render_template('deleteMenuItem.html', item = item, restaurant = restaurant)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
