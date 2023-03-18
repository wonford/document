# base of a dev / sandbox tool.
# want to quickly explore database structures.
# want to be able to quickly populate and query such structure
# want the query results (almost always heirarchical) to return as json
# for speed of dev, all relationships should be m2m
# ideally, these classes should also port to flask routes/models/foems pattern
# big ask.

from sqlalchemy import  *
from sqlalchemy.orm import *
from sqlalchemy.types import *

import sys
from datetime import datetime

import json
import inspect

dbEngine = create_engine('sqlite:///..\\io\\db\\alchemy.db', future=True)

Session = sessionmaker(bind=dbEngine, future=True)
session = Session()
Base = declarative_base()

#####################
# read some dummy data

def readJson():
    # just read in a hand-crafted json heirarchy
    f = open('table.json')
    data = json.load(f)
    f.close()
    print('JSON read')
    return data

def getInstanceVariables(pyClass):
    # bit of voodoo cut/paste code and nort necessarily safe ...
    attributes = inspect.getmembers(pyClass, lambda a: not (inspect.isroutine(a)))
    r = []
    for a in attributes:
        if not (a[0].startswith('_')) and a[0] not in ['metadata', 'registry', 'id']: r.append(a[0])
    return r


#######################
# stick data in db
# obvs the objects are hard-coded here
# but want to see how far I can go with a pattern of parent < m2m > child assembly
# so, hard code a single pre-known clas first

class Entity():
    # high level class that holds common methods
    def loadSelf(self, data):
        # assumes json matches sub class def (- kwargs?)
        for attr in getInstanceVariables(self):
            self.__dict__[attr] = data[attr]


#######################
# table classes (document -> frame)
# this does need to be defined here - just pushing in json data doesn't inform objects enough.
# next issue is relationships ...

class Document(Base, Entity):
    # AT the moment an example class of entity. Need to add parent and children constructors
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Frame(Base, Entity):
    # see above, but here just checking all runs through fine
    __tablename__ = 'frame'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cols = Column(Integer, default=0)
    rows = Column(Integer, default=0)



#######################
# Get data into objects ....

def loadObject(instanceClass, instanceData):
        item = instanceClass()
        item.loadSelf(instanceData)
        session.add(item)
        session.commit()


def loadData(data):
    for document in data['documents']:
        loadObject(Document, document)
        for frame in document['frames']:
            loadObject(Frame, frame)
    # ok, the population works fine - now the linking?
    # after that we can go recrsive on the hierarchy stack...
    # But!! where are we defining the structure?
    # How about a standard model which an read from json for sandpits? Then pt in interventions for les generalised stuff?








def run():
    print(f'Starting')
    # OK, read in a json heirarchy (hard code from other script for now)
    data = readJson()
    Base.metadata.create_all(dbEngine)
    loadData(data)
    print(f'Stopping')


if __name__ == '__main__':
    run()