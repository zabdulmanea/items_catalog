from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
 # Provider Table 
class Provider(Base):
    __tablename__ = 'provider'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(250))
 
 # Course Table
class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False, unique=True)  
    description = Column(String(250))
    provider_id = Column(Integer, ForeignKey('provider.id'))
    provider = relationship(Provider) 
 

engine = create_engine('sqlite:///providercourses.db')
Base.metadata.create_all(engine)