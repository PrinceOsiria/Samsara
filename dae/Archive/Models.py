###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# SQL-Alchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

###########################################################################################################################################
##################################################### Configuration #######################################################################
###########################################################################################################################################
# SQLite database creation and initialization
engine = create_engine('sqlite:///dae/Archive/archive.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

###########################################################################################################################################
##################################################### Functions ###########################################################################
###########################################################################################################################################
# Refresh database - WARNING THIS COMMAND DELETES EVERYTHING
def refresh_database():
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

# Add to database
def add_to_db(some_object):
	session.add(some_object)
	session.commit()

###########################################################################################################################################
##################################################### Associations ########################################################################
###########################################################################################################################################





###########################################################################################################################################
##################################################### Models ##############################################################################
###########################################################################################################################################
# Year Model
class Year(Base):
	__tablename__ = "Year"
	Year = Column(String, primary_key=True)
	drive_folder_id = Column(Integer)

	# Many
	months = None
	days = None
	events = None



# Month Model
class Month(Base):
	__tablename__ = "Month"
	Month = Column(String, primary_key=True)
	drive_folder_id = Column(Integer)

	# One
	year = None

	# Many
	days = None
	events = None



# Day Model
class Day(Base):
	__tablename__ = "Day"
	Day = Column(String, primary_key=True)
	drive_folder_id = Column(Integer)

	# One
	Year = None
	Month = None

	# Many
	Events = None



# Event Model
class Event(Base):
	__tablename__ = "Event"
	id = Column(Integer, primary_key=True)

	# Archive Information
	drive_event_folder_id = Column(String())
	drive_archive_folder_id = Column(String())
	drive_summary_document_id = Column(String())

	# Timeline Connections
	# One
	Year = None
	Month = None
	Day = None

	# Meta Information
	archived_on = Column(String())
	archived_by = Column(String())

	# Standard Information
	date = Column(String())
	title = Column(String())

	# Non-Standard Information
	evidence = Column(String())
	tags = Column(String())
	summary = Column(String())
