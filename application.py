from flask import Flask
app = Flask(__name__)


# view home page
@app.route('/')
@app.route('/providers')
def providers():
    return "providers page"


# view specific MOOC provider
@app.route('/provider/<string:provider_name>/')
@app.route('/provider/<string:provider_name>/courses/')
def viewProvider(provider_name):
    provider_name = "temp"
    return "courses of provider page"


# view specific MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/')
def viewCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return "Course Information page"


# Create MOOC course
@app.route('/provider/course/new/', methods=['GET', 'POST'])
def newCourse():
    return "Create New Course Page"


# Update information of MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/edit/', methods=['GET', 'POST'])
def editCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return "Update Course Information page"

# Delete specific MOOC course
@app.route('/provider/<string:provider_name>/course/<string:course_name>/delete/', methods=['GET', 'POST'])
def deleteCourse(provider_name, course_name):
    provider_name = "temp"
    course_name = "temp"
    return "Delete Course page"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
