from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Provider, Course

engine = create_engine('sqlite:///providercourses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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

# Search for provider
udacity = provider = session.query(Provider).filter_by(name='Udacity').one()

Courses = [
    {
        "name":
        "Machine Learning Engineer",
        "description":
        "In this program you will master Supervised, Unsupervised,"
        " Reinforcement, and Deep Learning fundamentals. You will also complete a "
        "capstone project in your chosen domain."
    },
    {
        "name":
        "Deep Learning",
        "description":
        "Deep learning is driving advances in artificial intelligence"
        " that are changing our world. Enroll now to build and apply your own deep neural "
        "networks to produce amazing solutions to important challenges."
    },
    {
        "name":
        "Data Analyst",
        "description":
        "Use Python, SQL, and statistics to uncover insights, communicate"
        " critical findings, and create data-driven solutions"
    },
    {
        "name":
        "Data Scientist",
        "description":
        "Build effective machine learning models, run data pipelines, build recommendation"
        " systems, and deploy solutions to the cloud with industry-aligned projects."
    },
    {
        "name":
        "Artificial Intelligence",
        "description":
        "Learn essential Artificial Intelligence concepts from AI experts like Peter Norvig and Sebastian Thrun,"
        " including search, optimization, planning, pattern recognition, and more."
    },
    {
        "name":
        "Become a Computer Vision Expert",
        "description":
        "Master the computer vision skills behind advances in robotics and automation. Write programs to analyze images,"
        " implement feature extraction, and recognize objects using deep learning models."
    },
    {
        "name":
        "Machine Learning Foundation",
        "description":
        "Udacity's Machine Learning Foundation Nanodegree is your first "
        "step towards careers in Data Analysis, Data Science, Machine Learning, AI, and more! "
        "This Nanodegree helps you learn Python and Statistics. It consists of 4 projects and "
        "is perfect for beginners in the field of data."
    }
]

for course in Courses:
    session.add(
        Course(
            name=course["name"],
            description=course["description"],
            provider=udacity,
            user=user1))
    session.commit()
