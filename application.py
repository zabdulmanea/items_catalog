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
    all_providers = session.query(Provider).all()
    # join_courses_providers = session.query(Course).join(Provider).filter(Course.provider_id==Provider.id).all()
    # result = session.execute('SELECT * FROM Course JOIN Provider ON Course.provider_id = Provider.id')
    # for _r in result:
    #     print(_r)
    latest_courses = session.query(Course).order_by(Course.id.desc()).limit(10)
    # for course in latest_courses:
    #     print course.name
    return render_template('index.html', providers=all_providers, latest_courses = latest_courses)


# view specific MOOC provider
@app.route('/provider/<string:provider_name>/')
@app.route('/provider/<string:provider_name>/courses/')
def viewProvider(provider_name):
    provider = session.query(Provider).filter_by(name=provider_name).one()
    courses = session.query(Course).filter_by(provider_id=provider.id).all()
    return render_template('viewprovider.html', provider = provider, courses = courses)


# view specific MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/')
def viewCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return render_template('viewcourse.html')


# create MOOC course
@app.route('/provider/course/new/', methods=['GET', 'POST'])
def newCourse():
    if request.method == 'POST':
        courseProvider = session.query(Provider).filter_by(id=request.form.get('selected-provider')).one()
        newCourse = Course(
            name=request.form['course_name'], description=request.form['course-description'], provider = courseProvider)
        session.add(newCourse)
        session.commit()
        return redirect(url_for('providers'))
    else:
        all_providers = session.query(Provider).all()
        return render_template('newcourse.html', providers = all_providers)

    


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
