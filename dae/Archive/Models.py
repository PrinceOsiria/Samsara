###########################################################################################################################################
##################################################### Imports #############################################################################
###########################################################################################################################################
# SQL-Alchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

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
##################################################### Models ##############################################################################
###########################################################################################################################################
# Root Drive Model
class Drive(Base):
	__tablename__ = "Drive"
	root_folder_id = Column(String, primary_key=True, unique=True)
	NITE_folder_id = Column(String, unique=True)
	evidence_folder_id = Column(String, unique=True)
	DAE_folder_id = Column(String, unique=True)
	archive_folder_id = Column(String, unique=True)
	current_events_file_id = Column(String, unique=True)
	years_file_id = Column(String, unique=True)
	template_folder_id = Column(String, unique=True)


# Year Model
class Year(Base):
	__tablename__ = "Year"
	# Drive Information
	drive_folder_id = Column(String, primary_key=True)

	# Timeline 
	year = Column(Integer, unique=True)
	months = relationship("Month", backref="year")
	days = relationship("Day", backref="year")
	events = relationship("Event", backref="year")

	# Document
	document_id = Column(String)



# Month Model
class Month(Base):
	__tablename__ = "Month"
	# Drive Information
	drive_folder_id = Column(String, primary_key=True)

	# Timeline
	year_id = Column(Integer, ForeignKey('Year.drive_folder_id'))
	month = Column(Integer)
	days = relationship("Day", backref="month")
	events = relationship("Event", backref="month")

	# Document
	document_id = Column(String)



# Day Model
class Day(Base):
	__tablename__ = "Day"
	# Drive Information
	drive_folder_id = Column(String, primary_key=True)

	# Timeline 
	year_id = Column(Integer, ForeignKey('Year.drive_folder_id'))
	month_id = Column(Integer, ForeignKey('Month.drive_folder_id'))
	day = Column(Integer)
	events = relationship("Event", backref="day")

	# Document
	document_id = Column(String)



# Event Model
class Event(Base):
	__tablename__ = "Event"
	id = Column(Integer, primary_key=True)

	# Timeline
	year_id = Column(Integer, ForeignKey('Year.drive_folder_id'))
	month_id = Column(Integer, ForeignKey('Month.drive_folder_id'))
	day_id = Column(Integer, ForeignKey('Day.drive_folder_id'))


	# Drive  Information
	drive_event_folder_id = Column(String())
	drive_archive_folder_id = Column(String())

	# Archive mimeType folders
	drive_archive_image_folder_id = Column(String())
	drive_archive_text_folder_id = Column(String())
	drive_archive_video_folder_id = Column(String())
	drive_archive_audio_folder_id = Column(String())

	# Source Evidence Files
	drive_archive_image_files_id_list = Column(MutableList.as_mutable(PickleType),default=[])
	drive_archive_video_files_id_list = Column(MutableList.as_mutable(PickleType),default=[])
	drive_archive_audio_files_id_list = Column(MutableList.as_mutable(PickleType),default=[])
	drive_archive_text_file_id = Column(String())

	# Formatted Media Files
	event_summary_file = Column(String())
	event_gif_file = Column(String())
	event_video_file = Column(String())
	event_audio_file = Column(String())
	event_audio_summary_file = Column(String())


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
