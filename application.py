from flask import Flask, render_template
app = Flask(__name__)


# view home page
@app.route('/')
@app.route('/providers')
def providers():
    return render_template('index.html')


# view specific MOOC provider
@app.route('/provider/<string:provider_name>/')
@app.route('/provider/<string:provider_name>/courses/')
def viewProvider(provider_name):
    provider_name = "temp"
    return render_template('viewprovider.html')


# view specific MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/')
def viewCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return render_template('viewcourse.html')


# create MOOC course
@app.route('/provider/course/new/', methods=['GET', 'POST'])
def newCourse():
    return render_template('newcourse.html')


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
