from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
app.secret_key = "super secret key"

CLIENT_ID = json.loads(
    open('client_secrets_ic.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalog"

engine = create_engine('sqlite:///catalogueitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """
    Login page for the app
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Google call to sign in the user using oauth2client
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets_ic.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])

    return output

# User Helper Functions


def createUser(login_session):
    """
    This method creates a new user
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    user = session.query(User).filter_by(email=email).one()
    return user.id


@app.route('/gdisconnect')
def gdisconnect():
    """
    This method calls the google api to sign out the user
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
          login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('allCategory'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given '
                                            'user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('allCategory'))


@app.route('/')
@app.route('/category/')
def allCategory():
    """
    This method calls the homepage of the application
    This page will list all the categories and the latest 10 items
    It also gives an option to add a new item for the logged in user
    """
    cats = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10).all()
    if 'username' not in login_session:
        return render_template('publiccategory.html', category=cats,
                               items=items)
    else:
        return render_template('category.html', category=cats, items=items)


@app.route('/category/<int:category_id>/')
def categoryList(category_id):
    """
    This method lists the items for a given category
    """
    cats = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=cats.id)
    return render_template('item.html', category=cats, items=items,
                           category_id=cats.id)


@app.route('/category/<int:category_id>/<int:item_id>/description')
def description(category_id, item_id):
    """
    This method gives the description for a given item
    For the logged in user, it gives the option to edit or delete the item
    :type item_id: object
    """
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('publicdescription.html',
                               category_id=category_id, item=item)
    else:
        return render_template('description.html', category_id=category_id,
                               item=item)


@app.route('/category/item/new/', methods=['GET', 'POST'])
def addItem():
    """
    This method lets the logged in user add a new item to a category
    """
    category_list = session.query(Category).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category_id = request.form.get('cat_name')
        cat = session.query(Category).filter_by(name=category_id).one()
        newItem = Item(
            name=request.form['name'], description=request.form['description'],
            category=cat,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % newItem.name)
        return redirect(url_for('allCategory'))
    else:
        return render_template('addItem.html', category_list=category_list)


@app.route('/category/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    """
    This method lets the logged in user(owner of the item) edit the item
    """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return render_template('error.html', message="edit")
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Item %s Successfully Edited' % editedItem.name)
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template(
            'editItem.html', category_id=category_id, item_id=item_id,
            item=editedItem)


@app.route('/category/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    """
    This method lets the logged in user(owner of the item) delete the item
    """
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return render_template('error.html', message="delete")
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item %s Successfully deleted' % itemToDelete.name)
        return redirect(url_for('allCategory'))
    else:
        return render_template('deleteItem.html', category_id=category_id,
                               item=itemToDelete)


@app.route('/category/<int:category_id>/items/JSON')
def itemJSON(category_id):
    """
    This method returns the items in Json format
    """
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/category/JSON')
def catJSON():
    """This method returns the categories in the Json format"""
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/category/<int:category_id>/<int:item_id>/description/JSON')
def descriptionJSON(category_id, item_id):
    """This method gives the description for a given item in Json format"""
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
