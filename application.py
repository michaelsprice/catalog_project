import string
import random
import requests
from flask import make_response
import json
import httplib2
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from flask import session as login_session
from database_setup import Base, Categories, Items, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, url_for, request, redirect, \
    jsonify, flash
from time import sleep
app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# Creates the connection to the database and creates the database session
engine = create_engine(
    'sqlite:///catalog.db',
    connect_args={
        'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Login page
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# gConnect page
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abandon ship.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is valid for the catalog app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # See if the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't, make a new user record
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; \
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print ("done!")
    return output


# Create a new user
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Get user info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Get user ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


# Disconnect the user by taking away the token and resetting their
# login_session
@app.route('/gdisconnect')
def gdisconnect():
    category = session.query(Categories)
    items = session.query(Items)
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s'), access_token
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Successfully logged out")
        return redirect(
            url_for(
                'showCategories',
                category=category,
                items=items))
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON API's for all categories
@app.route('/category/JSON')
def CategoryJSON():
    jsonCategory = session.query(Categories).all()
    return jsonify(Category=[i.serialize for i in jsonCategory])

# JSON API's to view the catalog items information
@app.route('/category/<int:categories_id>/items/JSON')
def CategoryItemsJSON(categories_id):
    jsonCategories = session.query(
        Categories).filter_by(id=categories_id).one()
    CategoryItems = session.query(Items).filter_by(
        category_id=jsonCategories.id).all()
    return jsonify(CategoryItems=[i.serialize for i in CategoryItems])

# JSON API's to view a single items information
@app.route('/category/<int:categories_id>/<int:item_id>/JSON')
def CategorySingleItemJSON(categories_id, item_id):
    jsonSingleItem = session.query(
        Categories).filter_by(id=categories_id).one()
    CategoryItem = session.query(Items).filter_by(id=jsonSingleItem.id).one()
    return jsonify(CategoryItem=[CategoryItem.serialize])

# Show all categories
@app.route('/')
@app.route('/categories')
def showCategories():
    category = session.query(Categories)
    items = session.query(Items)
    return render_template('categories.html', category=category, items=items)

# Show a category items
@app.route('/category/<int:categories_id>/items')
@app.route('/category/<int:categories_id>/')
def showCategoryItem(categories_id):
    categoryToShow = session.query(
        Categories).filter_by(id=categories_id).one()
    itemsToShow = session.query(Items).filter_by(category_id=categories_id)
    return render_template(
        'showCategoryItem.html',
        category=categoryToShow,
        items=itemsToShow)

# Create a new category item
@app.route('/category/<int:categories_id>/item/new', methods=['GET', 'POST'])
def createCategoryItem(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    theCategory = session.query(Categories).filter_by(id=categories_id).one()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            category_id=theCategory.id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(
            url_for(
                'showCategoryItem',
                categories_id=categories_id))
    else:
        return render_template(
            'createCategoryItem.html',
            categories_id=categories_id)

# Edit a category item


@app.route(
    '/category/<int:categories_id>/<int:item_id>/edit',
    methods=[
        'GET',
        'POST'])
def editCategoryItem(categories_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['Description']:
            editedItem.description = request.form['Description']
        session.add(editedItem)
        session.commit()
        return redirect(
            url_for(
                'showCategoryItem',
                categories_id=categories_id))
    else:
        return render_template(
            'editCategoryItem.html',
            categories_id=categories_id,
            item_id=item_id,
            i=editedItem)

# Delete a category item


@app.route(
    '/category/<int:categories_id>/<int:item_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteCategoryItem(categories_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please create your own item in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(
            url_for(
                'showCategoryItem',
                categories_id=categories_id))
    else:
        return render_template(
            'deleteCategoryItem.html',
            categories_id=categories_id,
            i=itemToDelete)

# Show an item and description
@app.route('/category/<int:categories_id>/<int:item_id>/description')
def showCategoryItemDescription(categories_id, item_id):
    category = session.query(Categories).filter_by(id=categories_id).one()
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    return render_template(
        'showCategoryItemDescription.html',
        category=category,
        items=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
