# Web Server modules
from flask import Flask, render_template, request, redirect, url_for, flash

# Database modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Provider, Course

# Library to generate unique session token
from flask import session as login_session
import random
import string

# Import OAuth libraries to handle the code sent back from callback method
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///providercourses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# declare CLIENT_ID using client_secrets file
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']


# ------------------- LOGIN -------------------------
# Make nti-forgery state token and view login page
@app.route('/login')
def viewLogin():
    # generate a random anti-forgery state token mixed of letters and digits
    state_token = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    # Set a login session state token
    login_session['state'] = state_token
    # render login page
    return render_template('login.html', STATE=state_token)


# Create G-connect that accepts one-time code
# and handle the code sent back from the callback method
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # ensure the user is making the request by validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # obtain one-time code
    code = request.data

    try:
        # exchange the authorization code into a credentials object which contains the access_token
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ensure the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ensure that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ensure that the access token's client ID is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # check is the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('You are already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # store the access token in the login session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 90px; height: 90px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# create G-disconnect
# revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # execute HTTP request to revoke current token
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('You are not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']

    # revoking token using google url
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print 'result is '
    print result

    if result['status'] == '200':
        # reset the user login_session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# ------------------- App Pages -------------------------
# view home page
@app.route('/')
@app.route('/providers')
def providers():
    # Get all providers
    all_providers = session.query(Provider).all()

    # Get the latest 10 courses along with each course provider
    latest_courses = session.query(
        Provider.name.label('provider_name'),
        Course.name.label('course_name')).filter(
            Course.provider_id == Provider.id).order_by(
                Course.id.desc()).limit(10)
    # render Home page
    return render_template(
        'index.html', providers=all_providers, latest_courses=latest_courses)


# view specific MOOC provider
@app.route('/provider/<string:provider_name>/')
@app.route('/provider/<string:provider_name>/courses/')
def viewProvider(provider_name):
    provider = session.query(Provider).filter_by(name=provider_name).one()
    courses = session.query(Course).filter_by(provider_id=provider.id).all()
    # render MOOC provider page
    return render_template(
        'viewprovider.html', provider=provider, courses=courses)


# view specific MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/')
def viewCourse(provider_name, course_name):
    course = session.query(Course).filter_by(name=course_name).one()
    # render course provider page
    return render_template(
        'viewcourse.html', provider_name=provider_name, course=course)


# create MOOC course
@app.route('/provider/course/new/', methods=['GET', 'POST'])
def newCourse():
    if 'username' not in login_session:
        return redirect(url_for('viewLogin'))

    if request.method == 'POST':
        # obtain the selected provider from the dropdown list
        courseProvider = session.query(Provider).filter_by(
            id=request.form.get('selected-provider')).one()
        # create a new provider course
        newCourse = Course(
            name=request.form['course_name'],
            description=request.form['course-description'],
            provider=courseProvider)
        session.add(newCourse)
        session.commit()
        # redirect to the main page
        return redirect(url_for('providers'))
    else:
        all_providers = session.query(Provider).all()
        # render creating course page
        return render_template('newcourse.html', providers=all_providers)


# update information of MOOC course
@app.route(
    '/provider/<string:provider_name>/course/<string:course_name>/edit/',
    methods=['GET', 'POST'])
def editCourse(provider_name, course_name):
    if 'username' not in login_session:
        return redirect(url_for('viewLogin'))
    # Get the course you want to update
    course = session.query(Course).filter_by(name=course_name).one()
    if request.method == 'POST':
        # obtain the selected provider from the dropdown list
        courseProvider = session.query(Provider).filter_by(
            id=request.form.get('selected-provider')).one()

        course.name = request.form['course_name']
        course.description = request.form['course-description']
        course.provider = courseProvider

        session.add(course)
        session.commit()

        # redirect to the course page
        return redirect(
            url_for(
                'viewCourse',
                provider_name=courseProvider.name,
                course_name=course_name))
    else:
        all_providers = session.query(Provider).all()
        # render updating course page
        return render_template(
            'editcourse.html',
            providers=all_providers,
            provider_name=provider_name,
            course=course)


# delete specific MOOC course
@app.route(
    '/provider/<string:provider_name>/course/<string:course_name>/delete/',
    methods=['GET', 'POST'])
def deleteCourse(provider_name, course_name):
    if 'username' not in login_session:
        return redirect(url_for('viewLogin'))
    if request.method == 'POST':
        course = session.query(Course).filter_by(name=course_name).one()
        session.delete(course)
        session.commit()
        # redirect to the provider page
        return redirect(url_for('viewProvider', provider_name=provider_name))
    else:
        # render deleting course page
        return render_template(
            'deletecourse.html',
            provider_name=provider_name,
            course_name=course_name)


# ------------------- Main -------------------------
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
