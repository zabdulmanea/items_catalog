# Web Server modules
from flask import Flask, render_template, request, redirect, url_for
# Database modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Provider, Course

app = Flask(__name__)

engine = create_engine('sqlite:///providercourses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


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
            Course.provider_id == Provider.id).order_by(Course.id.desc()).limit(10)

    return render_template(
        'index.html', providers=all_providers, latest_courses=latest_courses)


# view specific MOOC provider
@app.route('/provider/<string:provider_name>/')
@app.route('/provider/<string:provider_name>/courses/')
def viewProvider(provider_name):
    provider = session.query(Provider).filter_by(name=provider_name).one()
    courses = session.query(Course).filter_by(provider_id=provider.id).all()
    return render_template(
        'viewprovider.html', provider=provider, courses=courses)


# view specific MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/')
def viewCourse(provider_name, course_name):
    course = session.query(Course).filter_by(name=course_name).one()
    return render_template('viewcourse.html', provider_name = provider_name, course=course)


# create MOOC course
@app.route('/provider/course/new/', methods=['GET', 'POST'])
def newCourse():
    if request.method == 'POST':
        # get the selected proveder from the dropdown list
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
        return render_template('newcourse.html', providers=all_providers)


# update information of MOOC course
@app.route(
    '/provider/<string:provider_name>/course/<string:course_name>/edit/',
    methods=['GET', 'POST'])
def editCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return render_template('editcourse.html')


# delete specific MOOC course
@app.route(
    '/provider/<string:provider_name>/course/<string:course_name>/delete/',
    methods=['GET', 'POST'])
def deleteCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return render_template('deletecourse.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
