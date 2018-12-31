from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Provider, Course, User

engine = create_engine('sqlite:///provider_courses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

Providers = [
    {
        "name":
        "Edraak",
        "description":
        "Edraak, is a massive open online course (MOOC) platform, that is "
        "an initiative of the Queen Rania Foundation (QRF). QRF is determined to ensure "
        "that the Arab world is at the forefront of educational innovation. ",
        "link": "https://www.edraak.org/en/"
    },
    {
        "name":
        "Udacity",
        "description":
        "Udacity is where lifelong learners come to learn the skills they need,"
        " to land the jobs they want, to build the lives they deserve.",
        "link": "https://mena.udacity.com/"
    },
    {
        "name":
        "Coursera",
        "description":
        "Every course on Coursera is taught by top instructors from the world's best"
        " universities and educational institutions.",
        "link": "https://www.coursera.org/"
    },
    {
        "name":
        "edX",
        "description":
        "Increase access to high-quality education for everyone, everywhere"
        "Enhance teaching and learning on campus and online"
        "Advance teaching and learning through research",
        "link": "https://www.edx.org/"
    },
    {
        "name":
        "Iversity",
        "description":
        "Iversity supports higher education in the form of free "
        "Massive Open Online Courses (MOOCs) and launching new PRO Courses. ",
        "link": "https://iversity.org/"
    },
    {
        "name":
        "Canvas",
        "description":
        "Students in our courses gain instructional design experience while developing "
        "open educational resources for important social causes. When we decided to take our instructional "
        "design course to scale as a MOOC, Canvas Network quickly became our top choice.",
        "link": "https://www.canvas.net/"
    },
    {
        "name":
        "Open2Study",
        "description":
        "An initiative of Open Universities Australia, Open2Study brings you the best in "
        "online education with our four-week, introductory subjects.",
        "link": "https://www.open2study.com/"
    },
    {
        "name":
        "Open Learning",
        "description":
        "OpenLearning is an online learning platform that goes beyond content delivery "
        "to focus on community, connectedness, and student engagement.",
        "link": "https://www.openlearning.com/"
    }
]


session.query(Course).delete()
session.commit()

session.query(User).delete()
session.commit()

session.query(Provider).delete()
session.commit()

for provider in Providers:
    session.add(
        Provider(name=provider["name"], description=provider["description"], link=provider["link"]))
    session.commit()
