from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Provider, Course

engine = create_engine('sqlite:///provider_courses.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

table = session.execute('SELECT * FROM User')
print('----------START------------------')
for row in table:
   print(row)
   print('-----------------------------------------')