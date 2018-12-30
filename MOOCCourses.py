from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Provider, Course

engine = create_engine('sqlite:///provider_courses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# session.query(User).delete()
# session.commit()

# session.query(Provider).delete()
# session.commit()

# session.query(Course).delete()
# session.commit()

'''
# Insert user 1
user1 = User(
    name="Ali Ali",
    email="aali@udacity.com",
    picture=
    'https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)
session.add(user1)
session.commit()

# Insert user 2
user2 = User(
    name="Ahmed Hassan",
    email="ahassan@udacity.com",
    picture=
    'https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)
session.add(user2)
session.commit()
'''

# Providers
EDRAAK = session.query(Provider).filter_by(name='Edraak').one()
UDACITY = session.query(Provider).filter_by(name='Udacity').one()
COURSERA = session.query(Provider).filter_by(name='Coursera').one()
EDX = session.query(Provider).filter_by(name='edX').one()
IVERSITY = session.query(Provider).filter_by(name='Iversity').one()
CANVAS = session.query(Provider).filter_by(name='Canvas').one()
OPEN2STUDY = session.query(Provider).filter_by(name='Open2Study').one()
OPENLEARNING = session.query(Provider).filter_by(name='Open Learning').one()

udacityCourses = [
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    }

]

edrakCourses = [
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    }

]

courseraCourses = [
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    }

]

edXCourses = [
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    }

]

iversityCourses = [
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    }

]

canvasCourses = [
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    },
    {
        "name": "",
        "link": "",
        "description": ""
    }

]

# for course in udacityCourses:
#     session.add(
#         Course(
#             name=course["name"],
#             description=course["description"],
#             provider=udacity,
#             user=user1))
#     session.commit()
