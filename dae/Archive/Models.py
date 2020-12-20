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
##################################################### Model ###############################################################################
###########################################################################################################################################
# Data Model
class Event(Base):
	__tablename__ = "Event"
	id = Column(Integer, primary_key=True)

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

	def display(self):
		print(f"Archived on: {self.archived_on}\n Archived by: {self.archived_by}\n Date of Event: {self.date}\n Name of Event: {self.title}\n Tags: {self.tags}\n Evidence: {self.evidence}\n Summary: {self.summary}\n ")