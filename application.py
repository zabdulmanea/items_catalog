# Web Server modules
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

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

engine = create_engine('sqlite:///provider_courses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# ------------------- USER Functions -------------------------
# create a new user in the datbase ans get the user id
def createUser(login_session):
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# ------------------- LOGIN -------------------------

# declare CLIENT_ID using client_secrets file
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']


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


# ------------------- GOOGLE SIGNIN -------------------------
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

    # store user information in login_session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # check if user has account or create new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    # store user id in login_session
    login_session['user_id'] = user_id

    # view succeful login message
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img class="login_pic" src="'
    output += login_session['picture']
    output += '"<br>'
    flash("You are now logged in as %s" % login_session['username'])
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

    # revoking token using google url
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # reset the user login_session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You have been successfully logged out! ")
        return redirect(url_for('providers'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# ------------------- JSON | API Endpoint -------------------------
@app.route('/providers/JSON')
def providersJSON():
    providers = session.query(Provider).all()
    return jsonify(MOOCProviders=[p.serialize for p in providers])


@app.route('/provider/<string:provider_name>/JSON')
@app.route('/provider/<string:provider_name>/courses/JSON')
def providerCoursesJSON(provider_name):
    provider = session.query(Provider).filter_by(name=provider_name).one()
    courses = session.query(Course).filter_by(provider_id=provider.id).all()
    return jsonify(ProviderCourses=[c.serialize for c in courses])


@app.route('/provider/<string:provider_name>/course/<int:course_id>/JSON')
def courseJSON(provider_name, course_id):
    course = session.query(Course).filter_by(id=course_id).one()
    return jsonify(Course=course.serialize)


# ------------------- APP PAGES -------------------------
# view home page
@app.route('/')
@app.route('/providers')
def providers():    
    # Get all providers
    all_providers = session.query(Provider).all()

    # Get the latest 10 courses along with each course provider
    latest_courses = session.query(
        Provider.name.label('provider_name'),
        Course.name.label('course_name'), Course.id.label('course_id')).filter(
            Course.provider_id == Provider.id).order_by(
                Course.id.desc()).limit(10)
    # render Home page
    return render_template(
        'index.html',
        providers=all_providers,
        latest_courses=latest_courses,
        login_session=login_session)


# view specific MOOC provider
@app.route('/provider/<string:provider_name>/')
@app.route('/provider/<string:provider_name>/courses/')
def viewProvider(provider_name):
    provider = session.query(Provider).filter_by(name=provider_name).one()
    # courses = session.query(Course).filter_by(provider_id=provider.id).all()
    courses = session.query(
        Course.name.label('name'), User.name.label('user_name'), Course.id.label('id')).filter(
            Course.user_id == User.id,
            Course.provider_id == provider.id).all()

    # render MOOC provider page
    return render_template(
        'viewprovider.html',
        provider=provider,
        courses=courses,
        login_session=login_session)


# view specific MOOC course
@app.route('/provider/<string:provider_name>/course/<int:course_id>/')
def viewCourse(provider_name, course_id):
    course = session.query(Course).filter_by(id=course_id).one()
    course = session.query(
        Course.id.label('id'), Course.name.label('name'), Course.description, Course.link, Course.user_id, User.name.label('user_name')).filter(
            Course.user_id == User.id,
            Course.id == course_id).one()

    # render course provider page
    return render_template(
        'viewcourse.html',
        provider_name=provider_name,
        course=course,
        login_session=login_session)


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
            name=request.form['course-name'],
            description=request.form['course-description'],
            link=request.form['course-link'],
            provider=courseProvider,
            user_id=login_session['user_id'])
        session.add(newCourse)
        session.commit()
        flash("New Course %s Successfully Created!!" % newCourse.name)
        # redirect to the main page
        return redirect(url_for('providers'))
    else:
        all_providers = session.query(Provider).all()
        # render creating course page
        return render_template(
            'newcourse.html',
            providers=all_providers,
            login_session=login_session)


# update information of MOOC course
@app.route(
    '/provider/<string:provider_name>/course/<int:course_id>/edit/',
    methods=['GET', 'POST'])
def editCourse(provider_name, course_id):
    # check if the user is not logged in
    if 'username' not in login_session:
        return redirect(url_for('viewLogin'))

    # Get the course you want to update
    course = session.query(Course).filter_by(id=course_id).one()

    # check if the user is not authorized to edit
    if course.user_id != login_session['user_id']:
        flash("You are not allowed to edit this course!")
        return redirect(
            url_for(
                'viewCourse',
                provider_name=provider_name,
                course_id=course_id))

    if request.method == 'POST':
        # obtain the selected provider from the dropdown list
        courseProvider = session.query(Provider).filter_by(
            id=request.form.get('selected-provider')).one()
        course.name = request.form['course-name']
        course.description = request.form['course-description']
        course.link = request.form['course-link']
        course.provider = courseProvider
        session.add(course)
        session.commit()

        flash("%s Course Successfully Updated!!" % course.name)

        # redirect to the course page
        return redirect(
            url_for(
                'viewCourse',
                provider_name=courseProvider.name,
                course_id=course.id))
    else:
        all_providers = session.query(Provider).all()
        # render updating course page
        return render_template(
            'editcourse.html',
            providers=all_providers,
            provider_name=provider_name,
            course=course,
            login_session=login_session)


# delete specific MOOC course
@app.route(
    '/provider/<string:provider_name>/course/<int:course_id>/delete/',
    methods=['GET', 'POST'])
def deleteCourse(provider_name, course_id):
    # check if the user is not logged in
    if 'username' not in login_session:
        return redirect(url_for('viewLogin'))

    course = session.query(Course).filter_by(id=course_id).one()
    # check if the user is not authorized to delete
    if course.user_id != login_session['user_id']:
        flash("You are not allowed to delete this course!")
        # redirect to course page
        return redirect(
            url_for(
                'viewCourse',
                provider_name=provider_name,
                course_id=course_id))

    if request.method == 'POST':
        session.delete(course)
        session.commit()

        flash("%s Course Successfully Deleted!!" % course.name)

        # redirect to the provider page
        return redirect(url_for('viewProvider', provider_name=provider_name))
    else:
        # render deleting course page
        return render_template(
            'deletecourse.html',
            provider_name=provider_name,
            course=course,
            login_session=login_session)


# ------------------- Main -------------------------
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
