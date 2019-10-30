from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#associative_photo_post = Table('associative_photo_post', Base.metadata,
#                               Column('kvar_post', Integer, ForeignKey()),
#                               Column()
#                               )

class KvartiraPost(Base):

    __tablename__ = "kvpost"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    title = Column(String)
    #photos = relationship('Photos', backref='posts')


    author_url = Column(String)
    location = Column(String)

    def __init__(self, title, url, author_url, location):
        self.title = title
        self.url = url
        #self.photos.extend(photos)
        self.author_url = author_url
        self.location = location

class Photos(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)

    kvartira = Column(Integer, ForeignKey('kvpost.id'))

    def __init__(self, url, kvartirapost):
        self.url = url
        self.kvartira = kvartirapost.id