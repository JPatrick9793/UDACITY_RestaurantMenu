from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON page for all restaurants
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify( Restaurants = [r.serialize for r in restaurants] )


# JSON page for all menu items in particular restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


# JSON page for particular menu item from particular restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(Items = item.serialize)


# *** HOMEPAGE ***
# show all restaurants
@app.route('/')
@app.route('/restaurant')
@app.route('/restaurants')
def showRestaurants():
	# return "This page will show all my restaurants"
	restaurants = session.query(Restaurant)
	return render_template('index.html', restaurants = restaurants)


# create new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		flash("New Restaurant created!")
		# session.commit()

		# redirect to homepage
		return redirect(url_for('showRestaurants'))

	else:		
		# direct user to page for creating new restaurants
		return render_template('newRestaurant.html')


# edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		# session.commit()
		return redirect( url_for('showRestaurants') )
	return render_template('editRestaurant.html', restaurant = editedRestaurant)


# delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	# return "This page will be for deleting a particular restaurant"
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurant)
		flash("Restaurant deleted!")
		# session.commit()
		restaurants = session.query(Restaurant)
		return redirect( url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = restaurant)


# show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	# return "This page will show a particular restaurant's menu"
	return render_template('menu.html', items = items, restaurant = restaurant)


# create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		flash("New item created!!")
		# session.commit()
		return redirect( url_for('showMenu', restaurant_id = restaurant_id) )
	else:
		return render_template('newMenuItem.html', restaurant = restaurant)


# edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		editedItem.name = request.form['name']
		editedItem.description = request.form['description']
		editedItem.price = request.form['price']
		editedItem.course = request.form['course']
		session.add(editedItem)
		flash("Item edited!!")
		# session.commit()
		return redirect( url_for('showMenu', restaurant_id = restaurant_id) )
	else:
		return render_template('editMenuItem.html', item = editedItem, restaurant = restaurant)


# delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		session.delete(deletedItem)
		flash("Item deleted!!")
		# session.commit()
		return redirect( url_for('showMenu', restaurant_id = restaurant_id) )

	return render_template('deleteMenuItem.html', item = deletedItem, restaurant = restaurant)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
