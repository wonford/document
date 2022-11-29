# run through pandas / sqlAlchemy tutorial using sqlite

from sqlalchemy import  Table, Column, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.types import Integer, Text, String, DateTime

import sys
from datetime import datetime

dbEngine = create_engine('sqlite:///..\\io\\db\\doc01.db', future=True)

Session = sessionmaker(bind=dbEngine, future=True)
Base = declarative_base()


class Document(Base):
    # Holds the document meta-data
    pass

# One-to-many

class Frame(Base):
    # Gross arrangement level - effectively a 2-d ordering of items in hope
    # both tables inline paragraphs can be handled within one model
    # Contains sequences
    # Vast majority (0, 0) only
    pass

# One-to-one - maybe distinction not needed?

class Sequence(Base):
    # Ordering of paragraphs and sequences of within frames
    # May point to programatic sources for sequential repeats
    # Vast majority fault 0 length
    pass

# Many-to-many - paras may repeat across docs

class Paragraph(Base):
    # Styleing and numbering base unit. Arranged in sequences, composed of number of runs
    pass

# One-to-many

class Run(Base):
    # Inline styling, comments and substitution level
    # May point to progamatic sources
    pass

# One-to-many

class Substitution(Base):
    # actual substitution strings referncing run and client
    # May point to progamatic sources
    pass

# Many-to-many

class Client(Base):
    # client standing data
    pass

# No relationship as such - simply a log

class History(Base):
    # records all changes to db
    Pass






Base.metadata.create_all(dbEngine)

