from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Provider, Course

engine = create_engine('sqlite:///provider_courses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert user 1
user1 = User(
    name="Lujain Rehaily",
    email="lalrehaili@udacity.com",
    picture=
    'https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)
session.add(user1)
session.commit()

# Insert user 2
user2 = User(
    name="Somiah Al-Ali",
    email="salali@udacity.com",
    picture=
    'https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)
session.add(user2)
session.commit()

# Providers
EDRAAK = session.query(Provider).filter_by(name='Edraak').one()
UDACITY = session.query(Provider).filter_by(name='Udacity').one()
COURSERA = session.query(Provider).filter_by(name='Coursera').one()
EDX = session.query(Provider).filter_by(name='edX').one()
IVERSITY = session.query(Provider).filter_by(name='Iversity').one()
CANVAS = session.query(Provider).filter_by(name='Canvas').one()
OPEN2STUDY = session.query(Provider).filter_by(name='Open2Study').one()
OPENLEARNING = session.query(Provider).filter_by(name='Open Learning').one()

courses = [
    {
        "provider":
        UDACITY,
        "user":
        user1,
        "name":
        "Digital Marketing Nanodegree",
        "link":
        "https://mena.udacity.com/course/digital-marketing-nanodegree--nd018",
        "description":
        "Gain real-world experience running live campaigns as you learn from top experts in the field. Launch your career with a 360-degree understanding of digital marketing."
    },
    {
        "provider":
        UDACITY,
        "user":
        user2,
        "name":
        "Become a Digital Freelancer",
        "link":
        "https://mena.udacity.com/course/digital-freelancer-nanodegree--nd1017-mena",
        "description":
        "Take advantage of the flexibility, independence, mobility, and versatility that come with being a successful freelancer. Enroll in the Digital Freelancer Nanodegree program and learn the critical skills necessary to launch and advance a freelance career"
    },
    {
        "provider":
        EDRAAK,
        "user":
        user2,
        "name":
        "Success Skills and Self-improvement Specialization",
        "link":
        "https://www.edraak.org/en/specialization/specialization/successsp-vv1/",
        "description":
        "This uniquely tailored Specialization offers effective methods and practical ways that can help you finetune your personal skills and manage yourself productively enabling you to succeed in your personal and professional endeavours."
    },
    {
        "provider":
        EDRAAK,
        "user":
        user1,
        "name":
        "Public Speaking Skills",
        "link":
        "https://www.edraak.org/en/course/course-v1:Edraak+PS_SP+2018_SP/",
        "description":
        "Inspiring and motivating others start with the effective delivery of ideas and in today's market, effective presentations are part of the core of business competency. Public speaking skill is one of the greatest tools for any professional to leave a true powerful impact and it's the secret ingredient that makes any speech an unforgettable experience for the audience. Throughout the course, you'll learn new techniques, explore best practices of communication and content delivery and you will be trained to unleash your creativity in order to make your speech stand out."
    },
    {
        "provider":
        COURSERA,
        "user":
        user1,
        "name":
        "Developing Applications with Google Cloud",
        "link":
        "https://www.coursera.org/specializations/developing-apps-gcp",
        "description":
        "Design, Develop, and Deploy Apps on GCP. Build secure, scalable, and intelligent cloud-native applications."
    },
    {
        "provider":
        COURSERA,
        "user":
        user2,
        "name":
        "AWS Fundamentals: Going Cloud-Native",
        "link":
        "https://www.coursera.org/learn/aws-fundamentals-going-cloud-native",
        "description":
        "This course will introduce you to Amazon Web Services (AWS) core services and infrastructure. Through demonstrations you'll learn how to use and configure AWS services to deploy and host a cloud-native application. "
    },
    {
        "provider":
        IVERSITY,
        "user":
        user2,
        "name":
        "Critical Thinking for Business",
        "link":
        "https://iversity.org/en/courses/critical-thinking-for-business",
        "description":
        "Critical thinking is essential for optimising business models, communicating with clients and making overall better decisions. As one of the most valued skills today, learn how to test, discern and respond best in every professional situation."
    },
    {
        "provider":
        IVERSITY,
        "user":
        user1,
        "name":
        "Digital Marketing - Strategies & Channels",
        "link":
        "https://iversity.org/en/courses/digital-marketing-strategies-channels",
        "description":
        "Digital marketing has changed tremendously over the last few years. At the same time, there has never been more pressure on marketers to reach their goals. Learn the skills needed to make digital marketing strategies and channels effective today."
    },
    {
        "provider":
        EDX,
        "user":
        user1,
        "name":
        "Video Game Design History",
        "link":
        "https://www.edx.org/course/video-game-design-history",
        "description":
        "Learn about the evolution of video games from experts at The Strong National Museum of Play, the world's largest collection of video game materials."
    },
    {
        "provider":
        EDX,
        "user":
        user2,
        "name":
        "IoT Sensors and Devices",
        "link":
        "https://www.edx.org/course/sensors-and-devices-in-the-iot",
        "description":
        "Explore various IoT devices and sensor types, how they work, and how we connect them. Map out the process for developing your own IoT ideas."
    },
    {
        "provider":
        CANVAS,
        "user":
        user2,
        "name":
        "FUNDAMENTALS OF PHARMACOLOGY",
        "link":
        "https://www.canvas.net/browse/osu/global-one-health/courses/fundamentals-pharmacology",
        "description":
        "The Fundamentals of Pharmacology course overviews principles underlying drug action, including an investigation of current treatments for a variety of common diseases. In addition, this course will implement activities that apply pharmacological principles to discuss emerging therapeutic strategies and issues."
    },
    {
        "provider":
        CANVAS,
        "user":
        user1,
        "name":
        "GROWING WITH CANVAS",
        "link":
        "https://www.canvas.net/browse/canvasnet/courses/growing-with-canvas",
        "description":
        "Growing with Canvas has five modules of content that will take users through everything they need to know about using Canvas at their institutions - no matter what grade or level. The course uses a combination of the Canvas Video Guides and Canvas Guides to teach the content. Participants in the course will try out a number of the concepts through the practice activities."
    }
]

for course in courses:
    session.add(
        Course(
            name=course["name"],
            description=course["description"],
            link=course["link"],
            provider=course["provider"],
            user=course["user"]))
    session.commit()
