#######################################################
# 
# track.py
# Python implementation of the Class track
# Generated by Enterprise Architect
# Created on:      28-Sep-2020 10:48:26 PM
# Original author: natha
# 
#######################################################
from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Track(Base):
# default constructor  def __init__(self):  
    __tablename__ = "Track"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="track")
    course = Column(String(100))
    # 1-sigma error on a Gaussian distribution associated with the course attribute
    eCourse = Column(String(100))
    # 1-sigma error on a Gaussian distribution associated with the slope attribute
    eSlope = Column(String(100))
    # 1-sigma error on a Gaussian distribution associated with the speed attribute
    eSpeed = Column(String(100))
    speed = Column(String(100))
    version = Column(String(100))