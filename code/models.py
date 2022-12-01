# run through pandas / sqlAlchemy tutorial using sqlite

from sqlalchemy import  Table, Column, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.types import Integer, Text, String, DateTime, LargeBinary

import sys
from datetime import datetime

dbEngine = create_engine('sqlite:///..\\io\\db\\doc01.db', future=True)

Session = sessionmaker(bind=dbEngine, future=True)
Base = declarative_base()


class Document(Base):
    # Holds the document meta-data
    # and for now, pragmatically, should include blob of underlying doc temaplate with styles, headers, page nos, etc
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    template = Column(LargeBinary)

# One-to-many

class Frame(Base):
    # Gross arrangement level - effectively a 2-d ordering of items in hope
    # both tables inline paragraphs can be handled within one model
    # Contains sequences
    # Vast majority (0, 0) only
    __tablename__ = 'frame'

    id = Column(Integer, primary_key=True)
    documentId = (ForeignKey('document.id'))
    verticalOrder = Column(Integer, default=0)
    horizontalOrder = Column(Integer, default=0)

# One-to-one - maybe distinction not needed?

class Sequence(Base):
    # Ordering of paragraphs and sequences of within frames
    # May point to programatic sources for sequential repeats
    # Vast majority fault 0 length
    __tablename__ = 'sequence'

    id = Column(Integer, primary_key=True)

# Many-to-many - paras may repeat across docs

class Paragraph(Base):
    # Styleing and numbering base unit. Arranged in sequences, composed of number of runs
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True)

# One-to-many

class Run(Base):
    # Inline styling, comments and substitution level
    # May point to progamatic sources
    __tablename__ = 'run'

    id = Column(Integer, primary_key=True)

#Many-to-one from run

class Comment(Base):
    # Holds explanatory comments pinned to one or more runs
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

# One-to-many from run

class Substitution(Base):
    # actual substitution strings referncing run and client
    # May point to progamatic sources
    __tablename__ = 'substitution'

    id = Column(Integer, primary_key=True)

# Many-to-many

class Client(Base):
    # client standing data
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)

# No relationship as such - simply a log

class History(Base):
    # records all changes to db - this should be re-usabel across all projects
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    tableName  = Column(String)
    tableId    = Column(Integer)
    columnName = Column(String)
    originalValue = Column(String)
    amendedValue = Column(String)
    user = Column(String)
    time = Column(DateTime)  # will need to be looked at.







Base.metadata.create_all(dbEngine)

