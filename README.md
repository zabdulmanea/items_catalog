# Item Catalog (MOOC Providers Catalog)
###### Udacity's Full Stack Web Developer Nanodegree
----

## Project Description

Item Catalog is a data-driven web application that provides a list of courses within a variety of categories (Massive Open Online Course Providers) as well as integrates a third-party user registration and authentication with Google or Facebook. The app has been developed using Flask framework and accesses a SQL database that populates categories and their items. Authenticated users have the ability to create, update and delete their own posted courses. This project is guided by [Udacity’s Full Stack Developer Nanodegree Program](https://sa.udacity.com/course/full-stack-web-developer-nanodegree--nd004).


## Technologies Used

**Flask framework:** provides app routes to serve the HTTP endpoints and renders template to build the front-end pages
**OAuth:** implements Google/Facebook Login authentication and authorization systems for users
**SQLAlchemy:** communicating with the back-end database
**CRUD operations:** Manipulating database (Create, Read, Update and Delete)
**RESTful API endpoints:** return JSON files


## Files Included

| File | Description |
|------|-------------|
| **database_setup.py** | provides access to the database tables |
| **provider_courses.db** | the populated database file |
| **application.py** *(Main)* | runs Flask application |

## PreRequests
You need [VirtualBox](https://www.virtualbox.org/), [Vagrant](https://www.vagrantup.com/) and [Udacity Fullstack Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm) to run this project successfully.

## Getting Started
**1. Download [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)**
You are not required to run them.

**2. Install the VM configuration**
* Open terminal.
* Clone Udacity Fullstack VM configuration repository:  
`git clone https://github.com/udacity/fullstack-nanodegree-vm fullstack` 
* Change the directory to your vagrant directory `cd fullstack/vagrant`
* Run `vagrant up` - to install/run the Linux operating system.
* Run `vagrant ssh` - to log into your Linux VM!

**3. Clone the project repository to vagrant directory**  
* Change the directory to Linux vagrant directory `cd /vagrant`
`git clone https://github.com/zabdulmanea/items_catalog.git `

**5. Run Python Module**
* Change directory to the project directory:  
`cd /items_catalog`
* Run `python application.py`

**6. Access and launch the application on your web browser**
* Visit `http://localhost:8000/`

### JSON Endpoints
Returns JSON of all categories
```
http://localhost:8000/providers/JSON
```
Returns JSON of all items of specific category (i.e: all courses of udacity category)
```
http://localhost:8000/provider/udacity/JSON
```
Returns JSON of one course (i.e: Data Foundations course of udacity category)
```
http://localhost:8000/provider/Udacity/course/2/JSON
```
