# Web Server modules
from flask import Flask, render_template, request, redirect, url_for

# Database modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Provider, Course

# OAuth modules to generate unique session token
from flask import session as login_session
import random
import string

app = Flask(__name__)

engine = create_engine('sqlite:///providercourses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# ------------------- LOGIN -------------------------
# view login page
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
    if request.method == 'POST':
        # get the selected provider from the dropdown list
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
    # Get the course you want to update
    course = session.query(Course).filter_by(name=course_name).one()
    if request.method == 'POST':
        # get the selected provider from the dropdown list
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
